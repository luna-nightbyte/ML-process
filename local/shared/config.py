import os
import csv
import shared.file as files


from shared.constansts import Constansts

class Config:
    def __init__(self):
        """Initialize application settings with environment variables and default values."""
        # Paths and environment variables
        self.model_path = self._resolve_path("data", EnvManager.get(Constansts().ENV().MODEL_PATH))
        self.csv_file_path = self._resolve_path(os.path.join(Constansts().General().workDir,"data"), EnvManager.get(Constansts().ENV().CSV_FILE_PATH))
        self.source_folder = self._get_source_folder(EnvManager.get(Constansts().ENV().INPUT_DIR))
        self.dataset_target_folder = "./datasets"
        self.output_target_folder = self._resolve_path("./data/output", EnvManager.get(Constansts().ENV().SESSION_NAME))
        self.dataset_yaml = "./dataset.yaml"

        # App configurations
        self.app_name = EnvManager.get(Constansts().ENV().APP_NAME)
        self.session_name = EnvManager.get(Constansts().ENV().SESSION_NAME)
        self.extract_detection_img = EnvManager.get(Constansts().ENV().EXTRACT_BOX, cast_type=str) == "true"
        self.epochs = EnvManager.get(Constansts().ENV().EPOCHS, cast_type=int)
        self.threshold = EnvManager.get(Constansts().ENV().THRESHOLD, cast_type=float)
        self.batch = EnvManager.get(Constansts().ENV().BATCH, cast_type=int)
        self.min_consecutive = EnvManager.get(Constansts().ENV().CONSECUTIVE)
        # Model-related settings
        self.model_imge_size = EnvManager.get(Constansts().ENV().MODEL_IMG_SIZE, cast_type=int)
        self.model = None
        self.use_cuda = False

        # Output size and padding
        self.output_size, self.padding = self._parse_output_size(
            EnvManager.get(Constansts().ENV().OUTPUT_SIZE),
            EnvManager.get(Constansts().ENV().PADDING)
        )
        # Bounding box visibility
        self.show_bbox = self._parse_boolean(EnvManager.get(Constansts().ENV().SHOW_BOUNDING_BOX))

        # Server credentials
        files.Source().set_server_user(EnvManager.get(Constansts().ENV().SERVER_USER))
        files.Source().set_server_pass(EnvManager.get(Constansts().ENV().SERVER_PASS))

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
        self.writer = None
    def open(self, is_new_file: bool):
        """Open the CSV file for writing."""
        if self.is_open():
            return f"{self.path} already open"
        try:
            self.file = open(self.path, mode="a", newline="")
            fieldnames = [
                Constansts().CSV().ORIGINAL_FILEPATH,
                Constansts().CSV().FRAME_NUBMER,
                Constansts().CSV().DETECTION_NUMBER,
                Constansts().CSV().X1,
                Constansts().CSV().Y1,
                Constansts().CSV().X2,
                Constansts().CSV().Y2
            ]
            self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            if is_new_file:
                self.writer.writeheader()
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
    def write(self, path, frame_num, detection_num, x1,y1,x2,y2):
        err = self._write({
                    Constansts().CSV().ORIGINAL_FILEPATH: path,
                    Constansts().CSV().FRAME_NUBMER: frame_num, 
                    Constansts().CSV().DETECTION_NUMBER: detection_num, 
                    Constansts().CSV().X1: x1, 
                    Constansts().CSV().Y1: y1,
                    Constansts().CSV().X2: x2, 
                    Constansts().CSV().Y2: y2
                    }
                )
    def _write(self, data):
        """Write a row to the CSV file."""
        if not self.is_open():
            err = self.open(False)
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
                    data = self._parse_line(line)
                    output_data.append(data)
        except Exception as e:
            print(f"Error reading file {self.path}: {e}")
        return output_data


    def _parse_line(self, parts):
        """Parse a CSV line into a dictionary."""
        return {
            Constansts().CSV().ORIGINAL_FILEPATH: parts[0],
            Constansts().CSV().FRAME_NUBMER: parts[1], 
            Constansts().CSV().DETECTION_NUMBER: parts[2],
            Constansts().CSV().X1: parts[3],
            Constansts().CSV().Y1: parts[4],
            Constansts().CSV().X2: parts[5],
            Constansts().CSV().Y2: parts[6]
        }
        
csv_handler = CSV(settings.csv_file_path)