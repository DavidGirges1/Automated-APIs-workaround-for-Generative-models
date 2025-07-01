from asyncio import wait_for

from patchright.sync_api import sync_playwright
import pyperclip
import time


def initialize_browser():
    p = sync_playwright().start()
    context = p.chromium.launch_persistent_context(
        user_data_dir="mydata",
        channel="chrome",
        headless=False,
        no_viewport=True
    )
    page = context.new_page()
    page.goto("https://gemini.google.com/app")
    return p, context, page


def send_prompt_and_get_response(page, prompt,prompt_counter):
    locator = page.locator('div.ql-editor.textarea.new-input-ui[contenteditable="true"]')
    locator.wait_for()
    locator.click()
    locator.press('Control+A')
    locator.press('Backspace')
    locator.fill(prompt)
    locator.press("Enter")


    # working to fix the bug
    time.sleep(0.5)
    chat_div = page.locator("div.response-container").nth(prompt_counter-1)
    chat_div.wait_for()
    copy_button = chat_div.locator("copy-button >> button[data-test-id='copy-button'] >> mat-icon[data-mat-icon-name='content_copy']")
    copy_button.wait_for()
    copy_button.click()

    time.sleep(0.5)
    return pyperclip.paste()


# Interactive session
def chat_session():
    p, context, page = initialize_browser()
    prompt_counter = 0
    try:
        while True:
            prompt = input("\nEnter your prompt (or type 'exit' to quit): ").strip()
            if not prompt:  # If the input is empty after stripping, continue to the next loop iteration
                continue
            if prompt.lower() == 'exit':
                break
            prompt_counter += 1
            response = send_prompt_and_get_response(page, prompt,prompt_counter)
            print("\nGemini says:", response)


    finally:
        context.close()
        p.stop()


def single_chat():
    p, context, page = initialize_browser()
    prompt = input(""" 
            hello wrold
            
            """).strip()
    response = send_prompt_and_get_response(page, prompt, 1)
    print("\nGemini says:", response)


    context.close()
    p.stop()


def single_prompt(prompt: str) -> str:
    p, context, page = initialize_browser()
    try:
        response = send_prompt_and_get_response(page, prompt, 1)
        return response
    finally:
        context.close()
        p.stop()


prompt = """hello
world"""
single_prompt(prompt)
