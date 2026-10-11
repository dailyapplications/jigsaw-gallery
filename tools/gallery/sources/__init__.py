"""Museum / agency / Commons sources. Each module exposes `search(query, limit) -> list[Candidate]`.
(Art Institute of Chicago and Library of Congress are not used: their image servers block scripted downloads.)"""
from . import cleveland, commons, met, nasa, smk

SOURCES = {"commons": commons, "met": met, "cleveland": cleveland, "smk": smk, "nasa": nasa}
