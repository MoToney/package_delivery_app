from pathlib import Path

from config.load_config import load_config
from wgups.domain.address.Address import Address


class WGUPSConfig:
    """Centralized configuration management."""

    def __init__(self, project_root: Path):
        self.project_root: Path = project_root
        self.config: dict = load_config(project_root / "config/config.yaml")
        self.packages_path: Path = project_root / self.config["paths"]['packages_csv']
        self.distances_path: Path = project_root / self.config["paths"]['distances_csv']
        self.hub: Address = Address(
            street_address=self.config["hub"]["street_address"],
            city=self.config["hub"]["city"],
            state=self.config["hub"]["state"],
            zip_code=self.config["hub"]["zip_code"],
        )