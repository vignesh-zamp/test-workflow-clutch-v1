from playwright.async_api import async_playwright, Page
import os
import asyncio

class BrowserAgent:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def start(self, record_video_dir=None):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False) # Headless=False to see what's happening
        
        context_args = {"accept_downloads": True}
        if record_video_dir:
            context_args["record_video_dir"] = record_video_dir
            context_args["record_video_size"] = {"width": 1280, "height": 720}
            
        self.context = await self.browser.new_context(**context_args)
        self.page = await self.context.new_page()

    # Selectors from user's script
    SELECTORS = {
        "email_input": "input[type='email'], input[name='email']",
        "password_input": "input[type='password'], input[name='password']",
        "login_button": "button:has-text('Login')",
        "download_button": "#simple-tabpanel-1 > div > div > div > div.sc-aXZVg.sc-gEvEer.cYGXBL.hOYegP > button:nth-child(2)",
        "dl_files_link": "#taskGroup-3 > div > table > tbody > tr:nth-child(1) > td:nth-child(5)",
        "preview_button": "body > div.sc-BQMaI.eTiyZw.sc-fNZVXS.fGoHhh > div.MuiDialogContent-root.sc-epqpcT.dtZOCp > div > div.sc-dwalKd.keOGqW.modalContent > div > div:nth-child(1) > div:nth-child(1) > div.sc-lgPrIz.hHUCWw > div > div > div > button",
        "preview_close_button": "body > div:nth-child(23) > div.MuiDialogContent-root.sc-epqpcT.dtZOCp > div > div.sc-aXZVg.sc-gEvEer.sc-jdkBTo.hmRYzW.dSxcJT.bcPJgS > button",
        "dl_popup_close_button": "body > div.sc-BQMaI.eTiyZw.sc-fNZVXS.fGoHhh > div.MuiDialogContent-root.sc-epqpcT.dtZOCp > div > div.sc-aXZVg.sc-gEvEer.sc-jdkBTo.hmRYzW.dSxcJT.bcPJgS > button"
    }

    async def login(self, url, username, password):
        print(f"Navigating to {url}...")
        await self.page.goto(url)
        # Relaxed wait condition
        await self.page.wait_for_load_state("domcontentloaded")
        
        # Check if we are on a login page
        # Look for the "Welcome" header, email input, or "Sign in" / "Log in" text
        is_login_page = (
            await self.page.is_visible("text=Welcome") or 
            await self.page.is_visible("input[type='email']") or
            await self.page.is_visible("text=Sign in") or
            await self.page.is_visible("text=Log in")
        )
        
        if is_login_page:
            print("Login page detected. Logging in...")
            try:
                await self.page.fill("input[type='email']", username)
                await self.page.fill("input[type='password']", password)
                
                # Use get_by_role which is more robust
                # It matches button with name "Login" (case insensitive usually, or exact)
                await self.page.get_by_role("button", name="Login").click()
                
                # Wait for navigation, but don't be too strict about network idle
                await self.page.wait_for_load_state("domcontentloaded")
                print("Login submitted.")
                await self.page.wait_for_timeout(5000) # Increased wait to ensure redirect completes
            except Exception as e:
                print(f"Error during login: {e}")
                # Try fallback selector just in case
                try:
                    print("Trying fallback selector...")
                    await self.page.click("button")
                except:
                    pass
        else:
            print("No login form detected (already logged in?).")

        # Force navigation to the target URL if not there
        # Check if current URL matches target URL base (ignoring query params if needed, but here exact match is safer for tasks)
        if url not in self.page.url: 
            print(f"Current URL: {self.page.url}")
            print(f"Re-navigating to target: {url}...")
            await self.page.goto(url)
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_timeout(2000) # Wait for page to settle
            print(f"Arrived at {self.page.url}")

    async def capture_dl_screenshot(self, output_dir):
        """Captures screenshot of the Driver's License using user's flow."""
        print("Capturing DL screenshot...")
        path = os.path.join(output_dir, "dl_screenshot.png")
        
        try:
            print("Clicking Driver's License verification link...")
            await self.page.click(self.SELECTORS["dl_files_link"])
            
            print("Waiting for popup to load...")
            await asyncio.sleep(3)
            
            # Try to open preview, but if it fails, proceed with taking a screenshot of the popup
            try:
                print("Attempting to click Preview button...")
                preview_btn = self.page.locator(self.SELECTORS["preview_button"])
                # Hover over the button's parent or the button itself to trigger visibility
                await preview_btn.locator("..").hover() 
                await asyncio.sleep(0.5)
                
                if await preview_btn.is_visible():
                    await preview_btn.click()
                    print("Preview button clicked. Waiting for full image...")
                    await asyncio.sleep(3)
                else:
                    print("Preview button not visible. Will screenshot the popup thumbnail.")
            except Exception as e:
                print(f"Could not open preview (using thumbnail/popup view instead): {e}")

            # Take screenshot of whatever is visible (Full preview or Popup thumbnail)
            await self.page.screenshot(path=path, full_page=False)
            print(f"DL Screenshot saved to {path}")
            
            return path
            
        except Exception as e:
            print(f"Error capturing DL screenshot: {e}")
            # Fallback: save whatever is on screen
            await self.page.screenshot(path=path)
            return path
        finally:
            # Close popups - Critical to ensure next steps (download) work
            print("Closing popups...")
            try:
                # Press Escape multiple times to clear any overlays
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(0.5)
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(0.5)
                
                # Also try clicking the close button if visible
                if await self.page.is_visible(self.SELECTORS["dl_popup_close_button"]):
                    await self.page.click(self.SELECTORS["dl_popup_close_button"])
            except Exception as e:
                print(f"Warning closing popups: {e}")

    async def download_documents(self, output_dir):
        """Downloads all documents as a ZIP file."""
        print("Downloading documents (ZIP)...")
        try:
            print("Clicking Download button...")
            download_button = await self.page.wait_for_selector(self.SELECTORS["download_button"], timeout=10000)
            
            async with self.page.expect_download() as download_info:
                await download_button.click()
                download = await download_info.value
            
            path = os.path.join(output_dir, download.suggested_filename)
            await download.save_as(path)
            print(f"Downloaded ZIP to {path}")
            return path # Returns path to ZIP file
            
        except Exception as e:
            print(f"Failed to download documents: {e}")
            return None

    async def add_note_to_task(self, task_name, note_content):
        """Adds a note to a specific task line item."""
        print(f"Adding note to task: {task_name}")
        try:
            # 1. Find the row containing the task name
            # We look for a table row (tr) that contains the task_name text
            # Use .first to handle cases where multiple rows match (e.g. "second approval")
            row = self.page.locator(f"tr:has-text('{task_name}')").first
            
            # Ensure the row is visible
            if not await row.is_visible():
                print(f"Row for '{task_name}' not found or not visible.")
                return

            # 2. Find the Note button in that row.
            # We look for a button in the row. The note button usually has no text (just icon).
            # We can also target the last button or the one in the 8th column as per user hint.
            # Using the user's hint for DL: td:nth-child(8) > button
            # We'll try to be robust: find the button in the 8th column first.
            note_btn = row.locator("td:nth-child(8) > button")
            
            if not await note_btn.count():
                 # Fallback: Find any button in the row that is NOT the "Complete" or "Upload" button
                 # "Complete" is green/has text. Note button is icon only.
                 buttons = row.locator("button")
                 count = await buttons.count()
                 for i in range(count):
                     btn = buttons.nth(i)
                     txt = await btn.text_content()
                     if not txt.strip(): # Empty text usually means icon button
                         note_btn = btn
                         break
            
            await note_btn.click()
            
            # 3. Wait for Popup
            # User provided selector: textarea inside a form/dialog
            # Use :visible to ensure we target the one in the active dialog
            textarea_selector = "textarea[placeholder='Type your note...']:visible"
            await self.page.wait_for_selector(textarea_selector, state="visible", timeout=5000)
            
            # 4. Fill Note
            await self.page.fill(textarea_selector, note_content)
            
            # 5. Click Save
            # User provided: button with "SAVE NOTE"
            save_btn = self.page.locator("button", has_text="SAVE NOTE").locator("visible=true")
            
            # Wait for button to be enabled (remove Mui-disabled check if possible, or just wait for element to be enabled)
            # Playwright's click waits for actionability, but explicit wait helps if there's a transition
            await save_btn.wait_for(state="visible")
            
            # Sometimes the button takes a moment to become enabled after typing
            await self.page.wait_for_timeout(500)
            
            if await save_btn.is_disabled():
                 print("Save button is disabled. Waiting...")
                 await save_btn.wait_for(state="enabled", timeout=3000)

            await save_btn.click()
            
            # 6. Wait for dialog to close
            await self.page.wait_for_selector(textarea_selector, state="hidden", timeout=5000)
            print(f"Note added to '{task_name}'.")
            
            # Small delay to ensure UI settles
            await self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"Failed to add note to '{task_name}': {e}")
            # Try to close popup if stuck
            try:
                await self.page.keyboard.press("Escape")
            except:
                pass

    async def close(self):
        await self.browser.close()
