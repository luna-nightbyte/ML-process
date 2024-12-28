import os
import csv
import shared.file as files


class Config:
    def __init__(self):
        """Initialize application settings with environment variables and default values."""
        # Paths and environment variables
        self.model_path = self._resolve_path("data", EnvManager.get(EnvManager.MODEL_PATH))
        self.csv_file_path = self._resolve_path("/usr/src/app/data", EnvManager.get(EnvManager.CSV_FILE_PATH))
        self.source_folder = self._get_source_folder(EnvManager.get(EnvManager.INPUT_DIR))
        self.dataset_target_folder = "./datasets"
        self.output_target_folder = self._resolve_path("./data/output", EnvManager.get(EnvManager.SESSION_NAME))
        self.dataset_yaml = "./dataset.yaml"

        # App configurations
        self.app_name = EnvManager.get(EnvManager.APP_NAME)
        self.session_name = EnvManager.get(EnvManager.SESSION_NAME)
        self.extract_detection_img = EnvManager.get(EnvManager.EXTRACT_BOX, cast_type=str) == "true"
        self.epochs = EnvManager.get(EnvManager.EPOCHS, cast_type=int)
        self.threshold = EnvManager.get(EnvManager.THRESHOLD, cast_type=float)
        self.batch = EnvManager.get(EnvManager.BATCH, cast_type=int)
        self.min_consecutive = EnvManager.get(EnvManager.CONSECUTIVE)
        self.csv_fieldnames = ["file_path", "x1", "y1", "x2", "y2", "scale_x", "scale_y"]

        # Model-related settings
        self.model_imge_size = EnvManager.get(EnvManager.MODEL_IMG_SIZE, cast_type=int)
        self.model = None
        self.use_cuda = False

        # Output size and padding
        self.output_size, self.padding = self._parse_output_size(
            EnvManager.get(EnvManager.OUTPUT_SIZE),
            EnvManager.get(EnvManager.PADDING)
        )
        # Bounding box visibility
        self.show_bbox = self._parse_boolean(EnvManager.get(EnvManager.SHOW_BOUNDING_BOX))

        # Server credentials
        files.Source().set_server_user(EnvManager.get(EnvManager.SERVER_USER))
        files.Source().set_server_pass(EnvManager.get(EnvManager.SERVER_PASS))

        # Validations
        self._validate_input_files(self.source_folder)
        self.labels = files.get_labels(self.dataset_yaml)
        if not self.labels:
            print(f"Missing labels file {self.dataset_yaml}.")

        # Directory preparations
        self._prepare_directories()

    @staticmethod
    def _resolve_path(base, relative):
        """Resolve and join base and relative paths."""
        return os.path.join(base, relative)

    def _get_source_folder(self, input_dir):
        """Get the source folder path, handling numeric and string inputs."""
        try:
            return int(input_dir)
        except ValueError:
            return self._resolve_path("./data", input_dir)

    def _parse_output_size(self, output_size_env, padding_env):
        """Parse the output size and padding from environment variables."""
        if not output_size_env:
            return None, None
        try:
            size = [int(dim) for dim in output_size_env.split(",")]
            return (size[0], size[1]), padding_env
        except ValueError:
            raise ValueError("Invalid frame dimensions!")

    @staticmethod
    def _parse_boolean(value):
        """Parse a boolean value from a string."""
        return value and value.lower() == "true"

    def _validate_input_files(self, source_folder):
        """Validate the existence of input files."""
        if files.no_input_files(source_folder) and os.getenv("INPUT_DIR") != "0":
            raise FileNotFoundError(f"No video files in '{source_folder}'.")

    def _prepare_directories(self):
        """Ensure required directories exist."""
        for folder in [self.dataset_target_folder, self.output_target_folder, self.model_path]:
            files.create_if_not_exist(folder)


class EnvManager:
    """A class to handle environment variables."""

    MODEL_PATH: str = "MODEL_PATH"
    CSV_FILE_PATH = "CSV_FILE_PATH"
    SESSION_NAME = "SESSION_NAME"
    APP_NAME = "APP_NAME"
    INPUT_DIR = "INPUT_DIR"
    EPOCHS = "EPOCHS"
    BATCH = "BATCH"
    MODEL_IMG_SIZE = "MODEL_IMG_SIZE"
    CONSECUTIVE = "CONSECUTIVE"
    THRESHOLD = "THRESHOLD"
    OUTPUT_SIZE = "OUTPUT_SIZE"
    PADDING = "PADDING"
    EXTRACT_BOX = "EXTRACT_BOX"
    SHOW_BOUNDING_BOX = "SHOW_BOUNDING_BOX"
    SERVER_USER = "SERVER_USER"
    SERVER_PASS = "SERVER_PASS"
    
    @staticmethod
    def get(key, default=None, cast_type=str):
        value = os.getenv(key, default)
        if value is not None and cast_type:
            try:
                return cast_type(value)
            except ValueError:
                raise ValueError(f"Environment variable {key} could not be cast to {cast_type.__name__}")
        return value

    @staticmethod
    def set(key, value):
        os.environ[key] = str(value)

settings = Config()

class CSV:
    def __init__(self, path):
        """Initialize CSV data handler."""
        self.path = path
        self.file = None
        self.fieldnames = None
        self.writer = None

    def open(self, is_new_file: bool):
        """Open the CSV file for writing."""
        if self.is_open():
            return f"{self.path} already open"
        try:
            self.file = open(self.path, mode="a", newline="")
            self.writer = csv.DictWriter(self.file, fieldnames=settings.csv_fieldnames)
            if is_new_file:
                self.writer.writeheader()
            self.fieldnames = settings.csv_fieldnames
        except Exception as e:
            self.file = None
            print(f"Error opening file {self.path}: {e}")
            return str(e)
        return None
    def close(self):
        """Close the CSV file."""
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None

    def is_open(self):
        """Check if the CSV file is open."""
        return self.writer is not None

    def write(self, data):
        """Write a row to the CSV file."""
        if not self.is_open():
            err = self.open(False, self.fieldnames)
            if err:
                return str(err)
        try:
            self.writer.writerow(data)
        except Exception as e:
            return f"Error writing to file {self.path}: {e}"
        return None
    def read(self):
        """Read data from the CSV file."""
        output_data = []
        try:
            with open(self.path, mode="r") as file:
                reader = csv.reader(file)
                for line in reader:
                    if self._is_valid_input(line):
                        data = self._parse_line(line[0])
                        output_data.append(data)
        except Exception as e:
            print(f"Error reading file {self.path}: {e}")
        return output_data

    @staticmethod
    def _is_valid_input(line):
        """Validate the input line."""
        try:
            _ = int(line[0].split(",")[1])  # Test if input can be processed
            return True
        except (IndexError, ValueError):
            return False

    @staticmethod
    def _parse_line(line):
        """Parse a CSV line into a dictionary."""
        parts = line.split(",")
        return {
            "file_path": parts[0],
            "x1": int(parts[1]),
            "y1": int(parts[2]),
            "x2": int(parts[3]),
            "y2": int(parts[4]),
            "scale_x": float(parts[5]),
            "scale_y": float(parts[6]),
        }
        
csv_handler = CSV(settings.csv_file_path)