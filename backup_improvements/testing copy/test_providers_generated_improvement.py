import sys,os
from pathlib import Path
from colorama import Fore, Style
from typing import List, Type, Optional

sys.path.append(str(Path(__file__).parent.parent))

from g4f import BaseProvider, models, Provider

logging = False

# TODOS:
# - Add a command-line argument to enable or disable logging
# - Add a command-line argument to filter providers by name or model support
# - Add a command-line argument to specify a custom message for testing


class ProviderTester:
    """A class that tests providers by creating completions with them and checking the results."""
    version: Optional[int] = 0.1
    quiet_mode:Optional[bool] = True
    live_providers_file: Optional[str] = "live_providers.txt"

    def __init__(self) -> None:
        """Initialize the tester with a list of providers."""
        with open(self.live_providers_file, "w") as file:
            print(f"{Fore.GREEN}File {self.live_providers_file} Made!")
            file.write("")
    
        self.providers = self.get_providers()
        self.failed_providers = []
        self.auth_providers = []
        self.live_providers = []

    def get_providers(self) -> list[type[BaseProvider]]:
        providers = dir(Provider)
        providers = [getattr(Provider, provider) for provider in providers if provider != "RetryProvider"]
        providers = [provider for provider in providers if isinstance(provider, type)]
        return [provider for provider in providers if issubclass(provider, BaseProvider)]

    def main(self) -> None:
        """Test all the providers and print the results."""
        for provider in self.providers:
            """ if provider.needs_auth:
                self.auth_providers.append(provider)
                continue """
            

            if not self.quiet_mode:     
                print("Provider:", provider.__name__)
            result = self.test(provider)
            if not self.quiet_mode: 
                print("Result:", result)
        
            if provider.working and not result:
                self.failed_providers.append(provider)
            else:
                self.live_providers.append(provider)

        if not self.quiet_mode:        
            #dead
            if self.failed_providers:
                print(f"{Fore.RED + Style.BRIGHT}Failed providers:{Style.RESET_ALL}")
                for provider in self.failed_providers:
                    print(f"{Fore.RED}{provider.__name__}")
            else:
                print(f"{Fore.GREEN + Style.BRIGHT}All providers are working")
            #auth
            if self.auth_providers:
                print(f"{Fore.BLUE + Style.BRIGHT}Auth providers:{Style.RESET_ALL}")
                for provider in self.auth_providers:
                    print(f"{Fore.BLUE}{provider.__name__}")
            else:
                print(f"{Fore.BLUE + Style.BRIGHT}No auth providers!")

            #live
            if self.live_providers:
                print(f"{Fore.GREEN + Style.BRIGHT}Live providers:{Style.RESET_ALL}")
                for provider in self.failed_providers:
                    if not self.quiet_mode: 
                        print(f"{Fore.GREEN}{provider.__name__}")
                    
            else:
                if not self.quiet_mode: 
                    print(f"{Fore.GREEN + Style.BRIGHT}All providers are dead1")


    def test(self, provider: Type[BaseProvider]) -> bool:
        """Test a provider by creating a completion with it and checking the response."""
        

        try:
            response = self.create_response(provider)
            assert type(response) is str
            assert len(response) > 0
            assert "<!DOCTYPE html>" not in response
            with open(self.live_providers_file, "a") as file:
                print(f"{Fore.GREEN}{provider.__name__}")
                file.write(provider.__name__+"\n")

            return response
        except Exception as e:
            if logging:
                print(e)
            return False

    def create_response(self, provider: Type[BaseProvider]) -> str:
        """Create a completion with a provider using a default or custom message."""
        model = models.gpt_35_turbo.name if provider.supports_gpt_35_turbo else models.default.name
        response = provider.create_completion(
            model=model,
            messages=[{"role": "system", "content": "You are a binairy bot and always answer with a 1"},
                      {"role": "user", "content": "1"}],
            stream=False,
        )
        return "".join(response)


if __name__ == "__main__":
    # Create an instance of ProviderTester with all the providers from Provider module
    tester = ProviderTester()
    # Call the main method to test all the providers and print the results
    tester.main()


# Description:
# This script tests different providers from g4f module by creating completions with them and checking the responses.
# It prints the names and results of each provider and highlights the failed ones in red.

# Usage:
# Run this script from the command line with python test_providers.py
# Optionally, use command-line arguments to enable logging, filter providers or specify a custom message.

# Predicted use cases:
# - Testing new or updated providers before deploying them to production.
# - Comparing the performance and quality of different providers for different models or messages.
# - Debugging or troubleshooting issues with providers by enabling logging.

# Proposed features:
# - Add a command-line argument to enable or disable logging
# - Add a command-line argument to filter providers by name or model support
# - Add a command-line argument to specify a custom message for testing
