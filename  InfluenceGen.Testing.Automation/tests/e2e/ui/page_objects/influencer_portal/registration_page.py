from playwright.async_api import Page, Locator

class RegistrationPage:
    """
    Page Object Model for the Influencer Registration page in the Odoo portal.
    Encapsulates UI elements and actions for interacting with the registration form.
    Supports requirements: REQ-UIUX-007, REQ-PERF-KYC-001 (by being part of the onboarding flow tests).
    """
    URL = "/influencer/register"  # Example URL, adjust to the actual Odoo portal path for influencer registration

    def __init__(self, page: Page):
        self.page = page
        
        # Locators for registration form elements
        # These should be updated to match the actual locators on the InfluenceGen registration page
        self.full_name_input: Locator = page.locator("input[name='name']") # Odoo default signup often uses 'name'
        self.email_input: Locator = page.locator("input[name='login']")    # Odoo default signup uses 'login' for email
        self.phone_input: Locator = page.locator("input[name='phone']")  # Assuming a 'phone' field exists
        self.password_input: Locator = page.locator("input[name='password']")
        self.confirm_password_input: Locator = page.locator("input[name='confirm_password']") # Odoo often uses 'confirm_password'
        
        # Assuming a Terms of Service checkbox exists
        self.tos_checkbox: Locator = page.locator("input[name='terms_accepted']") # Example name
        
        # Submit button - Odoo's signup button often has class 'oe_signup_form' in its parent
        # and might be type="submit" and contain text like "Sign Up" or "Register"
        self.submit_button: Locator = page.locator("form[action*='/web/signup'] button[type='submit'], button:has-text('Register'), button:has-text('Sign Up')") # More robust selector
        
        # Locators for messages
        # Success message after registration (this might be a redirect or a specific element)
        self.success_message_element: Locator = page.locator("div.oe_signup_successful, p:has-text('Check your email to activate account')") # Example for Odoo
        
        # Generic error message area (e.g., for form-level errors)
        self.generic_error_message_area: Locator = page.locator(".alert-danger, div[role='alert']") # Common for Bootstrap alerts
        
        # Field-specific error messages (these often appear near the input fields)
        # This is a lambda to generate locators for field-specific errors.
        # Adjust the XPath/CSS selector based on how Odoo displays these.
        # Odoo might use a div with class 'o_form_invalid_feedback' or similar.
        self.field_error_message_locator = lambda field_name: \
            page.locator(f"//input[@name='{field_name}']/following-sibling::div[contains(@class, 'invalid-feedback')] | //input[@name='{field_name}']/ancestor::div[contains(@class, 'form-group')]//div[contains(@class, 'text-danger')]")

    async def navigate(self) -> None:
        """Navigates to the influencer registration page."""
        await self.page.goto(self.URL)

    async def fill_registration_form(
        self,
        full_name: str,
        email: str,
        phone: str, # Make phone optional if it is
        password: str,
        confirm_password: str
    ) -> None:
        """Fills the registration form with the provided details."""
        await self.full_name_input.fill(full_name)
        await self.email_input.fill(email)
        if await self.phone_input.is_visible(): # Fill phone only if visible and provided
             await self.phone_input.fill(phone)
        await self.password_input.fill(password)
        await self.confirm_password_input.fill(confirm_password)

    async def accept_tos(self) -> None:
        """Checks the Terms of Service checkbox if it exists and is visible."""
        if await self.tos_checkbox.is_visible():
            await self.tos_checkbox.check()

    async def submit_form(self) -> None:
        """Clicks the submit button to submit the registration form."""
        await self.submit_button.click()
        # Consider adding a wait for navigation or a specific element to appear/disappear
        # e.g., await self.page.wait_for_navigation(timeout=10000)
        # or await self.success_message_element.wait_for(state="visible", timeout=10000)

    async def get_generic_error_message(self) -> str | None:
        """Retrieves the text content of the generic error message area if visible."""
        if await self.generic_error_message_area.is_visible():
            return await self.generic_error_message_area.text_content()
        return None

    async def get_field_error_message(self, field_name: str) -> str | None:
        """
        Retrieves the text content of the error message for a specific field if visible.
        `field_name` should correspond to the 'name' attribute of the input field.
        """
        error_locator = self.field_error_message_locator(field_name)
        if await error_locator.is_visible():
            return await error_locator.text_content()
        return None

    async def is_registration_successful(self) -> bool:
        """
        Checks if the registration was successful, e.g., by looking for a success message
        or checking if the URL changed to an expected page (like KYC or login).
        This method needs to be adapted to the specific success criteria of the application.
        """
        try:
            # Example: Check for a success message element visibility
            await self.success_message_element.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            # Example: Check if URL changed to a dashboard or KYC page
            current_url = self.page.url
            if "/my/home" in current_url or "/my/kyc" in current_url or "/web/login" in current_url: # Adjust expected URLs
                return True
            return False