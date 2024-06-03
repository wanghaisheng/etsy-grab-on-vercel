import os
import tarfile
import tempfile
import requests
from urllib.parse import urlparse
from typing import Optional
from ssl import create_default_context
from selenium import webdriver


# Define the FollowRedirOptions type (for type hinting purposes)
class FollowRedirOptions:
    maxBodyLength: int
    netloc: str
    scheme: str


def is_valid_url(input: str) -> bool:
    try:
        result = urlparse(input)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_running_in_aws_lambda() -> bool:
    aws_execution_env = os.environ.get("AWS_EXECUTION_ENV")
    aws_lambda_js_runtime = os.environ.get("AWS_LAMBDA_JS_RUNTIME")

    if (
        aws_execution_env
        and "AWS_Lambda_nodejs" in aws_execution_env
        and "20.x" not in aws_execution_env
    ):
        return True
    elif (
        aws_lambda_js_runtime
        and "nodejs" in aws_lambda_js_runtime
        and "20.x" not in aws_lambda_js_runtime
    ):
        return True
    return False


def is_running_in_aws_lambda_node20() -> bool:
    aws_execution_env = os.environ.get("AWS_EXECUTION_ENV")
    aws_lambda_js_runtime = os.environ.get("AWS_LAMBDA_JS_RUNTIME")

    if aws_execution_env and "20.x" in aws_execution_env:
        return True
    elif aws_lambda_js_runtime and "20.x" in aws_lambda_js_runtime:
        return True
    return False


def download_and_extract(url: str) -> str:
    try:
        # Parse the URL and set maxBodyLength
        url_info = urlparse(url)
        options = FollowRedirOptions()
        options.maxBodyLength = 60 * 1024 * 1024  # 60mb
        options.netloc = url_info.netloc
        options.scheme = url_info.scheme

        # Create a directory to store the extracted files
        dest_dir = os.path.join(tempfile.gettempdir(), "chromium-pack")
        os.makedirs(dest_dir, exist_ok=True)

        # Download and extract the tarball
        with requests.get(url, stream=True, timeout=5) as r:
            r.raise_for_status()
            with tarfile.open(fileobj=r.raw, mode="r:*") as tar:
                tar.extractall(path=dest_dir)

        return dest_dir

    except Exception as e:
        # Clean up the destination directory if an error occurs
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        raise e


# Example usage
if __name__ == "__main__":
    url_to_download = "https://example.com/somefile.tar.gz"
    if is_valid_url(url_to_download):
        try:
            extraction_path = download_and_extract(url_to_download)
            print(
                f"Download and extraction complete. Files are located at: {extraction_path}"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid URL provided.")


import os
import requests
import tarfile

# file_path = os.path.join(os.pardir, "proxy_utils", "valid_proxy_list.txt")
# with open(file_path, "r") as f:
#     # read valid proxies into array
#     proxies = f.read().split("\n")
proxies = []


def getChomium():

    # from webdriver_manager.chrome import ChromeDriverManager

    # Specify a specific version of the Chrome WebDriver
    # URL of the tar file
    url = "https://github.com/Sparticuz/chromium/releases/download/v123.0.1/chromium-v123.0.1-pack.tar"

    # Download the tar file
    response = requests.get(url)
    with open("/tmp/chromium.tar", "wb") as file:
        file.write(response.content)

    # Extract the tar file
    with tarfile.open("/tmp/chromium.tar", "r") as tar:
        tar.extractall("/tmp")

    # Remove the tar file
    os.remove("/tmp/chromium.tar")

    # Get the directory name of the extracted package
    # Construct the path to the chromedriver executable
    webdriver_path = os.path.join("/tmp/chromium", "chromedriver")

    from selenium.webdriver.chrome.service import Service

    # Create a Service object with the WebDriver path
    service = Service(webdriver_path)

    # file_path = os.path.join(os.pardir, "proxy_utils", "valid_proxy_list.txt")
    # with open(file_path, "r") as f:
    #     # read valid proxies into array
    #     proxies = f.read().split("\n")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--verbose")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=options)
    from selenium_stealth import stealth

    stealth(
        driver,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=False,
        run_on_insecure_origins=False,
    )
