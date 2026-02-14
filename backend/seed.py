"""Seed script to populate the database with sample data for testing."""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.models import SessionLocal  # noqa: E402
from backend.models.fields import Field  # noqa: E402
from backend.models.matches import Match  # noqa: E402
from backend.models.players import Player  # noqa: E402
from backend.models.teams import Team  # noqa: E402
from backend.models.tournaments import Tournament, Registration  # noqa: E402
from backend.models.referees import Referee, Availability  # noqa: E402
from datetime import date  # noqa: E402


def seed():
    db = SessionLocal()
    try:
        # Teams
        teams_data = [
            {"name": "Defensor SC", "city": "Montevideo", "coach": "Carlos Lopez"},
            {"name": "Nacional", "city": "Montevideo", "coach": "Martin Silva"},
            {"name": "Penarol", "city": "Montevideo", "coach": "Diego Aguirre"},
            {"name": "Danubio FC", "city": "Montevideo", "coach": "Jorge Bava"},
            {"name": "Liverpool FC", "city": "Montevideo", "coach": "Pablo Repetto"},
            {"name": "Wanderers", "city": "Montevideo", "coach": "Daniel Carrenho"},
        ]
        teams = []
        for td in teams_data:
            t = Team(**td)
            db.add(t)
            teams.append(t)
        db.flush()

        # Players (2 per team)
        players_data = [
            ("Lucas Martinez", 0, 8, 3),
            ("Fernando Gomez", 0, 5, 7),
            ("Santiago Perez", 1, 12, 2),
            ("Matias Rodriguez", 1, 3, 5),
            ("Agustin Silva", 2, 15, 4),
            ("Diego Fernandez", 2, 7, 6),
            ("Nicolas Suarez", 3, 4, 3),
            ("Andres Garcia", 3, 6, 1),
            ("Pablo Gutierrez", 4, 9, 5),
            ("Juan Carlos", 4, 2, 8),
            ("Roberto Diaz", 5, 3, 2),
            ("Marcos Viera", 5, 1, 4),
        ]
        for name, team_idx, goals, assists in players_data:
            p = Player(
                name=name,
                team=teams[team_idx].name,
                team_id=teams[team_idx].id,
                goals=goals,
                assists=assists,
            )
            db.add(p)

        # Matches (some results)
        matches_data = [
            ("Defensor SC", "Nacional", 2, 1),
            ("Penarol", "Danubio FC", 3, 0),
            ("Liverpool FC", "Wanderers", 1, 1),
            ("Nacional", "Penarol", 0, 2),
            ("Defensor SC", "Liverpool FC", 1, 0),
            ("Danubio FC", "Wanderers", 2, 2),
        ]
        for home, away, hg, ag in matches_data:
            db.add(Match(home=home, away=away, home_goals=hg, away_goals=ag))

        # Fields
        fields_data = [
            {"name": "Cancha Central", "location": "Parque Batlle", "price_per_hour": 1500.0},
            {"name": "Complejo Rentistas", "location": "La Comercial", "price_per_hour": 1200.0},
            {"name": "Estadio Franzini", "location": "Pocitos", "price_per_hour": 2000.0},
        ]
        for fd in fields_data:
            db.add(Field(**fd))

        # Referees
        refs = [
            Referee(name="Esteban Ostojich", level="senior"),
            Referee(name="Andres Matonte", level="senior"),
            Referee(name="Gustavo Tejera", level="regional"),
        ]
        for r in refs:
            db.add(r)
        db.flush()

        # Availability
        for r in refs:
            for d in [date(2026, 3, 1), date(2026, 3, 8), date(2026, 3, 15)]:
                db.add(Availability(referee_id=r.id, date=d))

        # Tournament
        tournament = Tournament(name="Apertura 2026", format="round_robin", status="draft")
        db.add(tournament)
        db.flush()

        # Register all teams
        for t in teams:
            db.add(Registration(tournament_id=tournament.id, team_id=t.id))

        db.commit()
        print("Seed data inserted successfully!")
        print(f"  - {len(teams_data)} teams")
        print(f"  - {len(players_data)} players")
        print(f"  - {len(matches_data)} matches")
        print(f"  - {len(fields_data)} fields")
        print(f"  - {len(refs)} referees")
        print(f"  - 1 tournament with {len(teams_data)} registered teams")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
