from pathlib import Path

from config.load_config import load_config
from wgups.domain.address.Address import Address


class WGUPSConfig:
    """Centralized configuration management."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config = load_config(project_root / "config/config.yaml")
        self.packages_path = project_root / self.config["paths"]['packages_csv']
        self.distances_path = project_root / self.config["paths"]['distances_csv']
        self.hub = Address(
            street_address="1 Start Way",
            city="Salt Lake City",
            state="UT",
            zip_code="12345"
        )