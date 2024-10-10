# Project Name

This project is designed to manage and analyze various components and their attachments. It includes functionalities for handling different types of covers, zippers, velcro, and other related items.

## Project Structure

### Key Files and Directories

- **agents.py**: Contains agent-related functionalities.
- **attachments/**: Directory containing attachment-related documents.
  - **brief_description.txt**: Brief description of the attachments.
  - **Reference numbers.txt**: Reference numbers for various components.
- **docs/**: Documentation directory.
  - **final_report.txt**: Final report detailing various components and their descriptions.
- **graph.py**: Handles graph-related operations.
- **main.py**: Main entry point of the application.
- **notes.md**: Notes and additional information.
- **prompts.py**: Contains prompt-related functionalities.
- **rag.py**: Handles RAG (Red-Amber-Green) status operations.
- **requirements.txt**: Lists the dependencies required for the project.
- **state.py**: Manages the state of the application.
- **tools.py**: Utility tools for the project.
- **utils.py**: General utility functions.

## Getting Started

### Prerequisites

- Python 3.x
- Required dependencies listed in [`requirements.txt`]

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sushi057/Biggertuna
    ```
2. Navigate to the project directory:
    ```sh
    cd Biggertuna
    ```
3. Create virtual environment
    ```sh
    python -m venv .venv
    ```
4. Activate virtual environment
    ```sh
    source .venv/bin/activate
    ```
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

Run the main script to start the application:
```sh
python main.py
```