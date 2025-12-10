"""
LinkedIn Data Export Parser
Ingests LinkedIn data export CSVs and populates the human layer.

Usage:
    python -m context._brain.human.ingest.linkedin /path/to/linkedin-export/

Expected files in export directory:
    - Connections.csv
    - Messages.csv (optional, for relationship strength)
    - Positions.csv (optional, for experience)
    - Skills.csv (optional, for experience)
    - Profile.csv (optional, for experience)
"""

import csv
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Connection:
    """Represents a LinkedIn connection."""
    id: str
    name: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    connected_date: Optional[str] = None

    # Calculated from messages
    relationship_strength: str = "cold"
    message_count: int = 0
    last_message: Optional[str] = None

    # Manual enrichment (preserved if exists)
    context: str = ""
    domains: list = field(default_factory=list)
    can_ask_for: list = field(default_factory=list)
    has_asked_you: list = field(default_factory=list)
    introduces_to: list = field(default_factory=list)
    notes: str = ""
    last_contact: Optional[str] = None
    contact_frequency: Optional[str] = None

    # Positives & Negatives
    positives: list = field(default_factory=list)  # Strengths, superpowers
    negatives: list = field(default_factory=list)  # Watch-outs, friction points
    trust_level: Optional[str] = None  # high, medium, low, unknown
    energy: Optional[str] = None  # energizing, neutral, draining

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "position": self.position,
            "connected_date": self.connected_date,
            "relationship_strength": self.relationship_strength,
            "message_count": self.message_count,
            "last_message": self.last_message,
            "context": self.context,
            "domains": self.domains,
            "can_ask_for": self.can_ask_for,
            "has_asked_you": self.has_asked_you,
            "introduces_to": self.introduces_to,
            "notes": self.notes,
            "last_contact": self.last_contact,
            "contact_frequency": self.contact_frequency,
            # Positives & Negatives
            "positives": self.positives,
            "negatives": self.negatives,
            "trust_level": self.trust_level,
            "energy": self.energy,
        }


@dataclass
class Role:
    """Represents a work position."""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    domain: str = ""
    learned: list = field(default_factory=list)
    built: list = field(default_factory=list)
    failed_at: list = field(default_factory=list)
    relationships: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "company": self.company,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "domain": self.domain,
            "learned": self.learned,
            "built": self.built,
            "failed_at": self.failed_at,
            "relationships": self.relationships,
        }


class LinkedInParser:
    """Parser for LinkedIn data exports."""

    def __init__(self, export_path: str):
        self.export_path = Path(export_path)
        self.connections: dict[str, Connection] = {}
        self.roles: list[Role] = []
        self.skills: list[str] = []
        self.messages: dict[str, list] = defaultdict(list)  # name -> messages

    def _make_id(self, first_name: str, last_name: str) -> str:
        """Generate a connection ID from name."""
        clean = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
        return f"conn.{clean(first_name)}-{clean(last_name)}"

    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse various date formats to YYYY-MM-DD."""
        if not date_str:
            return None

        formats = [
            "%d %b %Y",  # 15 Jan 2023
            "%b %d, %Y",  # Jan 15, 2023
            "%Y-%m-%d",  # 2023-01-15
            "%m/%d/%Y",  # 01/15/2023
            "%d/%m/%Y",  # 15/01/2023
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

        return date_str  # Return as-is if can't parse

    def parse_connections(self) -> int:
        """Parse Connections.csv."""
        csv_path = self.export_path / "Connections.csv"
        if not csv_path.exists():
            print(f"Warning: {csv_path} not found")
            return 0

        count = 0
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row.get('First Name', '').strip()
                last_name = row.get('Last Name', '').strip()

                if not first_name:
                    continue

                conn_id = self._make_id(first_name, last_name)

                # Handle duplicate names by appending number
                base_id = conn_id
                counter = 2
                while conn_id in self.connections:
                    conn_id = f"{base_id}-{counter}"
                    counter += 1

                self.connections[conn_id] = Connection(
                    id=conn_id,
                    name=f"{first_name} {last_name}",
                    first_name=first_name,
                    last_name=last_name,
                    email=row.get('Email Address', '').strip() or None,
                    company=row.get('Company', '').strip() or None,
                    position=row.get('Position', '').strip() or None,
                    connected_date=self._parse_date(row.get('Connected On', '')),
                )
                count += 1

        print(f"Parsed {count} connections from Connections.csv")
        return count

    def parse_messages(self) -> int:
        """Parse Messages.csv and calculate relationship strength."""
        csv_path = self.export_path / "Messages.csv"
        if not csv_path.exists():
            # Try alternate name
            csv_path = self.export_path / "messages.csv"
            if not csv_path.exists():
                print("Warning: Messages.csv not found - relationship strength will default to 'cold'")
                return 0

        count = 0
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # LinkedIn message format varies, try common column names
                sender = row.get('From', row.get('SENDER', row.get('Sender', ''))).strip()
                date = row.get('Date', row.get('DATE', row.get('Sent Date', ''))).strip()

                if sender:
                    self.messages[sender].append({
                        'date': self._parse_date(date),
                        'sender': sender,
                    })
                    count += 1

        # Calculate relationship strength
        now = datetime.now()
        six_months_ago = now - timedelta(days=180)

        for conn_id, conn in self.connections.items():
            name = conn.name
            msgs = self.messages.get(name, [])

            if not msgs:
                # Also check first name only (messages sometimes use first name)
                msgs = self.messages.get(conn.first_name, [])

            conn.message_count = len(msgs)

            if msgs:
                # Find most recent message
                dates = [m['date'] for m in msgs if m['date']]
                if dates:
                    conn.last_message = max(dates)

                # Calculate relationship strength
                if len(msgs) >= 10:
                    conn.relationship_strength = "close"
                elif len(msgs) >= 3:
                    conn.relationship_strength = "warm"
                else:
                    conn.relationship_strength = "cold"

        print(f"Parsed {count} messages from Messages.csv")
        return count

    def parse_positions(self) -> int:
        """Parse Positions.csv for work history."""
        csv_path = self.export_path / "Positions.csv"
        if not csv_path.exists():
            print("Warning: Positions.csv not found")
            return 0

        count = 0
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('Company Name', '').strip()
                title = row.get('Title', '').strip()

                if not company or not title:
                    continue

                self.roles.append(Role(
                    company=company,
                    title=title,
                    start_date=self._parse_date(row.get('Started On', '')),
                    end_date=self._parse_date(row.get('Finished On', '')),
                ))
                count += 1

        print(f"Parsed {count} positions from Positions.csv")
        return count

    def parse_skills(self) -> int:
        """Parse Skills.csv."""
        csv_path = self.export_path / "Skills.csv"
        if not csv_path.exists():
            print("Warning: Skills.csv not found")
            return 0

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                skill = row.get('Name', row.get('Skill', '')).strip()
                if skill:
                    self.skills.append(skill)

        print(f"Parsed {len(self.skills)} skills from Skills.csv")
        return len(self.skills)

    def parse_all(self):
        """Parse all available LinkedIn export files."""
        print(f"\nParsing LinkedIn export from: {self.export_path}\n")

        self.parse_connections()
        self.parse_messages()
        self.parse_positions()
        self.parse_skills()

        print(f"\nTotal: {len(self.connections)} connections, {len(self.roles)} roles, {len(self.skills)} skills")

    def compute_stats(self) -> dict:
        """Compute network statistics."""
        stats = {
            "total": len(self.connections),
            "by_relationship": {
                "cold": 0,
                "warm": 0,
                "close": 0,
            },
            "by_domain": {},
            "stale_relationships": [],
        }

        six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

        for conn in self.connections.values():
            stats["by_relationship"][conn.relationship_strength] += 1

            # Track stale (no message in 6 months but was warm/close)
            if conn.relationship_strength in ("warm", "close"):
                if conn.last_message and conn.last_message < six_months_ago:
                    stats["stale_relationships"].append(conn.id)

            # Count domains
            for domain in conn.domains:
                stats["by_domain"][domain] = stats["by_domain"].get(domain, 0) + 1

        return stats

    def export_network(self, output_path: str, preserve_manual: bool = True):
        """Export connections to network.yaml."""
        output = Path(output_path)

        # Load existing to preserve manual enrichments
        existing = {}
        if preserve_manual and output.exists():
            with open(output, 'r') as f:
                data = yaml.safe_load(f)
                if data and data.get('connections'):
                    for conn in data['connections']:
                        existing[conn['id']] = conn

        # Merge: new data overwrites LinkedIn fields, preserves manual fields
        connections = []
        for conn_id, conn in self.connections.items():
            conn_dict = conn.to_dict()

            if conn_id in existing:
                # Preserve manual enrichments
                old = existing[conn_id]
                for field in ['context', 'domains', 'can_ask_for', 'has_asked_you',
                              'introduces_to', 'notes', 'last_contact', 'contact_frequency',
                              'positives', 'negatives', 'trust_level', 'energy']:
                    if old.get(field):
                        conn_dict[field] = old[field]

            connections.append(conn_dict)

        # Sort by relationship strength, then name
        strength_order = {'close': 0, 'warm': 1, 'cold': 2}
        connections.sort(key=lambda c: (strength_order.get(c['relationship_strength'], 3), c['name']))

        stats = self.compute_stats()

        network_data = {
            "version": "1.0",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "source": "linkedin_export",
            "connections": connections,
            "stats": stats,
            "network_gaps": [],
            "import_log": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "linkedin_export",
                    "connections_added": len(connections) - len(existing),
                    "connections_updated": len(existing),
                }
            ],
        }

        with open(output, 'w') as f:
            yaml.dump(network_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"\nExported {len(connections)} connections to {output}")

    def export_experience(self, output_path: str, preserve_manual: bool = True):
        """Export positions and skills to experience.yaml."""
        output = Path(output_path)

        # Load existing to preserve manual enrichments
        existing_roles = {}
        existing_skills = {}
        if preserve_manual and output.exists():
            with open(output, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    for role in data.get('roles', []):
                        key = f"{role.get('company')}|{role.get('title')}"
                        existing_roles[key] = role
                    existing_skills = data.get('skills', {})

        # Merge roles
        roles = []
        for role in self.roles:
            role_dict = role.to_dict()
            key = f"{role.company}|{role.title}"

            if key in existing_roles:
                old = existing_roles[key]
                for field in ['domain', 'learned', 'built', 'failed_at', 'relationships']:
                    if old.get(field):
                        role_dict[field] = old[field]

            roles.append(role_dict)

        # Merge skills
        skills = {
            "linkedin": self.skills,
            "technical": existing_skills.get('technical', []),
            "domain": existing_skills.get('domain', []),
            "soft": existing_skills.get('soft', []),
            "strong": existing_skills.get('strong', []),
            "developing": existing_skills.get('developing', []),
            "gaps": existing_skills.get('gaps', []),
            "overrated": existing_skills.get('overrated', []),
        }

        experience_data = {
            "version": "1.0",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "source": "linkedin_export",
            "roles": roles,
            "skills": skills,
            "education": {
                "formal": [],
                "self_taught": [],
                "learning_now": [],
            },
            "meta": {
                "confidence": "grounded",
                "last_validated": datetime.now().strftime("%Y-%m-%d"),
            },
        }

        with open(output, 'w') as f:
            yaml.dump(experience_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"Exported {len(roles)} roles and {len(self.skills)} skills to {output}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m context._brain.human.ingest.linkedin <path-to-linkedin-export>")
        print("\nTo get your LinkedIn export:")
        print("1. Go to LinkedIn -> Settings & Privacy")
        print("2. Click 'Data privacy' in left sidebar")
        print("3. Click 'Get a copy of your data'")
        print("4. Select 'Download larger data archive'")
        print("5. Wait for email, download, and extract the ZIP")
        sys.exit(1)

    export_path = sys.argv[1]

    if not os.path.isdir(export_path):
        print(f"Error: {export_path} is not a directory")
        sys.exit(1)

    # Determine output paths
    script_dir = Path(__file__).parent.parent
    network_output = script_dir / "network.yaml"
    experience_output = script_dir / "experience.yaml"

    # Parse and export
    parser = LinkedInParser(export_path)
    parser.parse_all()
    parser.export_network(network_output)
    parser.export_experience(experience_output)

    print("\n--- Summary ---")
    stats = parser.compute_stats()
    print(f"Total connections: {stats['total']}")
    print(f"  Close: {stats['by_relationship']['close']}")
    print(f"  Warm: {stats['by_relationship']['warm']}")
    print(f"  Cold: {stats['by_relationship']['cold']}")
    if stats['stale_relationships']:
        print(f"\nStale relationships (warm/close but no message in 6 months): {len(stats['stale_relationships'])}")

    print("\nDone! Run the intelligence layer to get insights:")
    print("  python -m context._brain.human.analysis.network_intel")


if __name__ == "__main__":
    main()
