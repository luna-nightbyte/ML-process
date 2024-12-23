
## Docker install
#### Steps:

**For macOS:**

1. [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) and install it.
2. Once installed, start Docker Desktop from your Applications folder.
3. Ensure Docker is running by checking the Docker icon in the menu bar.

**For Windows:**

1. [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) and install it.
2. Ensure your system supports WSL 2. You may need to enable it as Docker Desktop requires it for running Linux containers.
3. Start Docker Desktop from your Start Menu.
4. Confirm Docker is running by checking the Docker icon in the system tray.

**For Ubuntu:**

1. Open a terminal and run the following commands to install Docker:

    ```bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    ```

2. Log out and log back in to apply the group membership changes.
3. Confirm Docker is installed by running:

    ```bash
    docker --version
    ```

4. Install Docker Compose by running:

    ```bash
    sudo apt-get install -y docker-compose
    ```

5. Confirm Docker Compose is installed by running:

    ```bash
    docker-compose --version
    ```
