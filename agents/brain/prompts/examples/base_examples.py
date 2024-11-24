import json

class ExamplesBase:
    """Base class for defining examples used in prompt generation."""

    def __init__(self):
        self.tool_examples = []
        self.module_examples = []
        self.file_examples = {
            "prd": """
            # prd
            - **Title**: Inventory Management System (IMS)
            - **Introduction**: The IMS is designed to streamline inventory tracking, reduce stock discrepancies,
              and optimize supply chain operations for businesses of all sizes.
            - **Goals**:
              - Provide real-time tracking of inventory across multiple warehouses.
              - Support automated restocking based on predefined thresholds.
              - Enable detailed reporting for inventory analysis and decision-making.
            - **Features**:
              - Inventory Tracking: Monitor stock levels, item locations, and movement across warehouses.
              - Multi-Warehouse Support: Manage inventory across multiple storage facilities.
              - Automated Restocking: Trigger purchase orders when stock levels fall below thresholds.
              - Barcode Integration: Support scanning for fast and accurate stock updates.
              - Reporting: Generate detailed reports on stock levels, turnover rates, and reorder points.
              - Role-Based Access: Secure the system with roles such as Admin, Manager, and Viewer.
            """,
            "uml_class": """
            # uml diagrams
            - **Class Diagram**:
              ```mermaid
              classDiagram
                class InventoryManager {
                  +viewInventory(): List
                  +updateStock(itemId: int, quantity: int): bool
                  +generateReport(startDate: Date, endDate: Date): Report
                }

                class Item {
                  +id: int
                  +name: string
                  +quantity: int
                  +location: Location
                }

                class Location {
                  +id: int
                  +name: string
                  +address: string
                }

                class Report {
                  +generateTurnoverReport(startDate: Date, endDate: Date): List
                }

                InventoryManager --> Item : manages >>
                InventoryManager --> Report : creates >>
                Item --> Location : stored_in >>
              ```,
            "uml_sequence": ""
            - **Sequence Diagram**:
              ```mermaid
              sequenceDiagram
                participant User
                participant API
                participant InventoryManager
                participant Database

                User->>API: Request inventory data
                API->>InventoryManager: Fetch inventory data
                InventoryManager->>Database: Query stock levels
                Database-->>InventoryManager: Return stock data
                InventoryManager-->>API: Send inventory data
                API-->>User: Display inventory levels

                User->>API: Update stock levels
                API->>InventoryManager: Validate update
                InventoryManager->>Database: Update stock records
                Database-->>InventoryManager: Confirmation
                InventoryManager-->>API: Success response
                API-->>User: Stock update successful
              ```
            """,
            "architecture": """
            # Inventory Management System (IMS) - Architecture
            - **Description**: The architecture for the IMS is designed for scalability, reliability, and real-time inventory tracking.
            - **Components**:
              - **Frontend**: A React.js web interface for managing and viewing inventory.
              - **Backend**: A Python-based Flask API for business logic and database interactions.
              - **Database**: PostgreSQL for storing inventory, location, and user data.
              - **WebSocket Server**: Enables real-time updates for stock changes.
            - **File Structure**:
              ```
              ├── ims
              │   ├── __init__.py
              │   ├── app.py
              │   ├── models.py
              │   ├── routes
              │   │   ├── inventory.py
              │   │   └── reports.py
              ├── static
              │   ├── js
              │   │   └── app.js
              │   └── css
              │       └── styles.css
              └── tests
                  ├── test_inventory.py
                  └── test_reports.py
              ```
            """,
            "code_output": """
            ### Inventory Management System (IMS) - Code Output
            - **main.py**:
              ```python
              from ims import app

              if __name__ == "__main__":
                  app.run(debug=True)
              ```

            - **models.py**:
              ```python
              from sqlalchemy import Column, Integer, String
              from ims import db

              class Item(db.Model):
                  id = Column(Integer, primary_key=True)
                  name = Column(String(80))
                  quantity = Column(Integer)
                  location = Column(String(120))
              ```
            """,
            "requirements": """
            ### Inventory Management System (IMS) - Requirements.txt
            ```
            Flask==2.1.1
            SQLAlchemy==1.4.32
            psycopg2-binary==2.9.3
            ```
            """,
            "acceptance_test": """
            # Acceptance Tests
            ```python
            import subprocess
            import sys
            def run_lice(arguments):
                cmd = [sys.executable, 'lice/core.py'] + arguments
                result = subprocess.run(cmd, capture_output=True, text=True)
                return result.stdout, result.stderr, result.returncode

            def test_default_license_generation():
                stdout, stderr, returncode = run_lice([])
                assert "All rights reserved." in stdout
                assert returncode == 0

            def test_specified_license_generation():
                stdout, stderr, returncode = run_lice(['mit'])
                assert "Permission is hereby granted" in stdout
                assert returncode == 0

            if __name__ == "__main__":
                test_default_license_generation()
                test_specified_license_generation()
                ```
            """,
            "unit_test": """
            # Unit Tests
            ```python
            import unittest
            from lice.core import clean_path, extract_vars, generate_license
            class TestCoreFunctions(unittest.TestCase):
                def test_clean_path(self):
                    self.assertEqual(clean_path("."), os.getcwd())
                def test_generate_license(self):
                    template = "{{ year }} - {{ project }}"
                    context = {"year": "2024", "project": "TestProject"}
                    self.assertEqual(generate_license(template, context), "2024 - TestProject")
            if __name__ == "__main__":
                unittest.main()
            ```
            """
        }

    def add_tool_example(self, user_input: str, tool_name: str, refined_prompt: str):
        """Add a tool example to the list of tool examples."""
        example = {
            "use_tool": True,
            "tool_name": tool_name,
            "refined_prompt": refined_prompt
        }
        self.tool_examples.append(self.format_example(user_input, example))

    def add_module_example(self, user_input: str, lobe_index: int, refined_prompt: str):
        """Add a module example to the list of module examples."""
        example = {
            "use_tool": False,
            "lobe_index": lobe_index,
            "refined_prompt": refined_prompt
        }
        self.module_examples.append(self.format_example(user_input, example))

    @staticmethod
    def format_example(user_input: str, response: dict) -> str:
        """Helper to format an example entry."""
        response_str = json.dumps(response, indent=4)
        return f"User input: \"{user_input}\"\nResponse:\n{response_str}\n"

    def get_examples(self) -> str:
        """Return a formatted string of examples for both tools and modules. Overrides this method in child classes."""
        examples_str = "\n".join(self.tool_examples + self.module_examples)
        return examples_str if examples_str else "No examples available."

    def get_prd(self) -> str:
        """
        Retrieves PRD examples. If an example name is provided, it retrieves a specific example.

        Returns:
        - A dictionary of the requested PRD example or the whole PRD category.
        """
        return self.file_examples["prd"]

    def get_uml(self) -> str:
        """
        Retrieves UML examples.

        Returns:
        - A dictionary of the requested UML example or the whole UML category.
        """
        uml = self.file_examples["uml_class"] + self.file_examples["uml_sequence"]
        return uml

    def get_uml_class(self) -> str:
        """
        Retrieves UML Class examples.

        Returns:
        - A dictionary of the requested UML Class example or the whole UML Class category.
        """
        return self.file_examples["uml_class"]

    def get_uml_sequence(self) -> str:
        """
        Retrieves UML Sequence examples.

        Returns:
        - A dictionary of the requested UML Sequence example or the whole UML Sequence category.
        """
        return self.file_examples["uml_sequence"]


    def get_architecture(self) -> str:
        """
        Retrieves Architecture examples.

        Returns:
        - A dictionary of the requested Architecture example or the whole Architecture category.
        """
        return self.file_examples["architecture"]

    def get_code_output(self) -> str:
        """
        Retrieves Code Output examples.

        Returns:
        - A dictionary of the requested Code Output example or the whole Code Output category.
        """
        return self.file_examples["code_output"]

    def get_requirements_txt(self) -> str:
        """
        Retrieves Requirements examples.

        Returns:
        - A dictionary of the requested Requirements example or the whole Requirements category.
        """
        return self.file_examples["requirements"]

    def get_acceptance_test(self) -> str:
        """Returns Acceptance Test example."""
        return self.file_examples.get("acceptance_test", "No Acceptance Test example available.")

    def get_unit_test(self) -> str:
        """Returns Unit Test example."""
        return self.file_examples.get("unit_test", "No Unit Test example available.")



