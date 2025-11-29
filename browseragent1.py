import asyncio
import uuid
from playwright.async_api import async_playwright
from datetime import datetime
import os

# Configuration
USERNAME = "benjamin.koppeser+zamp@clutch.ca"
PASSWORD = "MUSASHI-detailed-regiment-bothers-1!"
TARGET_URL = "https://admin.staging.clutchenv.ca/private-purchases/59213148-6383-40fe-80f3-cc699c52abdb/tasks"

# Generate unique batch ID
BATCH_ID = str(uuid.uuid4())[:8]
SCREENSHOT_NAME = f"DL_screenshot_{BATCH_ID}.png"
VIDEO_NAME = "Login1.webm"

# Selectors
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


async def main():
    print(f"Starting automation with Batch ID: {BATCH_ID}")
    print(f"Screenshot will be saved as: {SCREENSHOT_NAME}")
    print(f"Video will be saved as: {VIDEO_NAME}")
    
    async with async_playwright() as p:
        # Launch browser with video recording
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir="./videos/",
            record_video_size={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        try:
            # Step 1: Navigate to login page
            print("\n[1/8] Navigating to login page...")
            await page.goto("https://admin.staging.clutchenv.ca/")
            await page.wait_for_load_state('networkidle')
            
            # Step 2: Login
            print("[2/8] Logging in...")
            await page.fill(SELECTORS["email_input"], USERNAME)
            await page.fill(SELECTORS["password_input"], PASSWORD)
            await page.click(SELECTORS["login_button"])
            
            # Wait for login to complete
            print("    Waiting for login redirect...")
            await page.wait_for_load_state('networkidle', timeout=15000)
            await asyncio.sleep(2)
            
            # Step 3: Navigate to target URL
            print(f"[3/8] Navigating to target URL...")
            await page.goto(TARGET_URL)
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # Step 4: Click Download button
            print("[4/8] Clicking Download button...")
            download_button = await page.wait_for_selector(SELECTORS["download_button"], timeout=10000)
            
            # Set up download listener
            async with page.expect_download() as download_info:
                await download_button.click()
                download = await download_info.value
                
            # Save the download
            download_path = f"./downloads/{download.suggested_filename}"
            os.makedirs("./downloads", exist_ok=True)
            await download.save_as(download_path)
            print(f"    Downloaded: {download.suggested_filename}")
            
            # Step 5: Click on Driver's License 1/1 file(s) link
            print("[5/8] Clicking Driver's License verification link...")
            await page.click(SELECTORS["dl_files_link"])
            
            # Wait for popup to appear
            print("    Waiting for popup to load...")
            await asyncio.sleep(3)
            
            # Step 6: Click Preview button
            print("[6/8] Clicking Preview button...")
            preview_button = await page.wait_for_selector(SELECTORS["preview_button"], timeout=10000)
            await preview_button.click()
            
            # Wait for full image to load
            print("    Waiting for full image to load...")
            await asyncio.sleep(3)
            
            # Step 7: Take screenshot
            print(f"[7/8] Taking screenshot: {SCREENSHOT_NAME}")
            os.makedirs("./screenshots", exist_ok=True)
            await page.screenshot(path=f"./screenshots/{SCREENSHOT_NAME}", full_page=False)
            print(f"    Screenshot saved successfully!")
            
            # Step 8: Close popups
            print("[8/8] Closing popups...")
            
            # Close the preview (full image view)
            try:
                preview_close = await page.wait_for_selector(SELECTORS["preview_close_button"], timeout=5000)
                await preview_close.click()
                await asyncio.sleep(1)
                print("    Closed preview popup")
            except Exception as e:
                print(f"    Warning: Could not close preview popup: {e}")
            
            # Close the DL popup
            try:
                dl_close = await page.wait_for_selector(SELECTORS["dl_popup_close_button"], timeout=5000)
                await dl_close.click()
                await asyncio.sleep(1)
                print("    Closed DL popup")
            except Exception as e:
                print(f"    Warning: Could not close DL popup: {e}")
            
            print("\n✅ Automation completed successfully!")
            print(f"   Batch ID: {BATCH_ID}")
            print(f"   Screenshot: ./screenshots/{SCREENSHOT_NAME}")
            print(f"   Download: {download_path}")
            
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            print(f"   Taking error screenshot...")
            try:
                await page.screenshot(path=f"./screenshots/error_{BATCH_ID}.png")
            except:
                pass
            raise
        
        finally:
            # Close browser and save video
            await context.close()
            await browser.close()
            
            # Rename video file
            print("\nProcessing video recording...")
            video_dir = "./videos"
            if os.path.exists(video_dir):
                videos = [f for f in os.listdir(video_dir) if f.endswith('.webm')]
                if videos:
                    latest_video = max([os.path.join(video_dir, f) for f in videos], key=os.path.getctime)
                    new_video_path = f"./videos/{VIDEO_NAME}"
                    os.rename(latest_video, new_video_path)
                    print(f"   Video saved: {new_video_path}")


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("./videos", exist_ok=True)
    os.makedirs("./screenshots", exist_ok=True)
    os.makedirs("./downloads", exist_ok=True)
    
    asyncio.run(main())