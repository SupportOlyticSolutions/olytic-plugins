#!/usr/bin/env python3
"""
Olytic Telemetry Startup Script

This script runs when Claude Cowork starts (via SessionStart hook).
It reads all staged telemetry files from ~/.claude/telemetry/,
sends them to Supabase, and cleans up local files.

Credentials are read from the .env file (not in git, stored separately).
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / '.claude' / 'telemetry.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TelemetryStartup:
    def __init__(self):
        self.telemetry_dir = Path.home() / '.claude' / 'telemetry'
        # Credentials are stored in ~/Olytic Setup/.env on the user's machine
        self.env_path = Path.home() / 'Olytic Setup' / '.env'
        self.supabase_url = None
        self.supabase_api_key = None
        self.files_sent = 0
        self.events_sent = 0
        self.errors = []

    def load_credentials(self):
        """Load Supabase credentials from .env file."""
        if not self.env_path.exists():
            logger.warning(f'.env file not found at {self.env_path}. Skipping telemetry transmission.')
            return False

        try:
            with open(self.env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('SUPABASE_URL='):
                        self.supabase_url = line.split('=', 1)[1].strip('"\'')
                    elif line.startswith('SUPABASE_API_KEY='):
                        self.supabase_api_key = line.split('=', 1)[1].strip('"\'')

            if not self.supabase_url or not self.supabase_api_key:
                logger.warning('Incomplete Supabase credentials in .env. Skipping transmission.')
                return False

            logger.info('Credentials loaded successfully.')
            return True
        except Exception as e:
            logger.error(f'Failed to load credentials: {e}')
            return False

    def find_staged_files(self):
        """Find all .jsonl files in the telemetry staging directory."""
        if not self.telemetry_dir.exists():
            logger.info(f'Telemetry directory {self.telemetry_dir} does not exist. Nothing to send.')
            return []

        files = list(self.telemetry_dir.glob('*.jsonl'))
        logger.info(f'Found {len(files)} telemetry file(s) to process.')
        return files

    def read_telemetry_file(self, file_path):
        """Read JSONL telemetry file and return list of events."""
        events = []
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError as e:
                        logger.error(f'Invalid JSON in {file_path} line {line_num}: {e}')
                        self.errors.append(f'{file_path}: line {line_num} - {e}')
            logger.info(f'Read {len(events)} events from {file_path.name}')
            return events
        except Exception as e:
            logger.error(f'Failed to read {file_path}: {e}')
            self.errors.append(f'Read error: {file_path} - {e}')
            return []

    def send_to_supabase(self, events):
        """Send events to Supabase. (Placeholder for actual implementation)"""
        if not events:
            return True

        try:
            import requests
        except ImportError:
            logger.warning('requests library not available. Skipping Supabase transmission.')
            logger.info(f'Would send {len(events)} events to Supabase (mock).')
            return True

        try:
            headers = {
                'Authorization': f'Bearer {self.supabase_api_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }

            # Supabase insert endpoint
            url = f'{self.supabase_url}/rest/v1/telemetry_events'

            # Send events as array
            response = requests.post(url, json=events, headers=headers, timeout=30)

            if response.status_code in [200, 201]:
                logger.info(f'Successfully sent {len(events)} events to Supabase.')
                return True
            else:
                logger.error(f'Supabase returned {response.status_code}: {response.text}')
                self.errors.append(f'Supabase error: {response.status_code}')
                return False
        except Exception as e:
            logger.error(f'Failed to send events to Supabase: {e}')
            self.errors.append(f'Transmission error: {e}')
            return False

    def cleanup_file(self, file_path):
        """Delete a telemetry file after successful transmission."""
        try:
            file_path.unlink()
            logger.info(f'Deleted {file_path.name}')
            return True
        except Exception as e:
            logger.error(f'Failed to delete {file_path}: {e}')
            self.errors.append(f'Cleanup error: {file_path.name} - {e}')
            return False

    def run(self):
        """Main startup sequence."""
        logger.info('=== Telemetry Startup Process ===')
        logger.info(f'Telemetry directory: {self.telemetry_dir}')

        # Step 1: Load credentials
        if not self.load_credentials():
            logger.info('Skipping telemetry transmission (no credentials).')
            return 0

        # Step 2: Find staged files
        staged_files = self.find_staged_files()
        if not staged_files:
            return 0

        # Step 3: Process each file
        for file_path in staged_files:
            logger.info(f'\nProcessing {file_path.name}...')

            # Read events
            events = self.read_telemetry_file(file_path)
            if not events:
                logger.warning(f'No valid events in {file_path.name}, skipping.')
                continue

            # Send to Supabase
            if self.send_to_supabase(events):
                # Clean up on success
                if self.cleanup_file(file_path):
                    self.files_sent += 1
                    self.events_sent += len(events)
            else:
                logger.warning(f'Failed to send {file_path.name}, keeping local file.')

        # Summary
        logger.info(f'\n=== Telemetry Startup Complete ===')
        logger.info(f'Files sent: {self.files_sent}')
        logger.info(f'Events sent: {self.events_sent}')
        if self.errors:
            logger.warning(f'Errors encountered: {len(self.errors)}')
            for error in self.errors:
                logger.warning(f'  - {error}')

        return 0 if not self.errors else 1


if __name__ == '__main__':
    startup = TelemetryStartup()
    sys.exit(startup.run())
