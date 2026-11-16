"""The game versions this repo builds from ONE shared src/ tree (sotn-decomp / psx_tomba multi-version scheme).

Each version is keyed by its lower-case disc serial. The reference version (PAL, sces01331) keeps the historical
layout (config/<prog>.yaml, asm/<prog>/, build/); every other version has config/<serial>/ (splat configs,
symbol_addrs_<prog>.txt, reuse.txt), asm/<serial>/<prog>/ and build/<serial>/. The C of every version lives in src/:
the build defines VERSION_<SERIAL> (tools/ncheck.py EXTRA_CPP) and a file can carry `#if defined(VERSION_SLPS_01144)`
branches (written by tools/version_share.py). See docs/JP.md, docs/JPDEMO.md and the README.

Per version: the game dir, the macro serial, the old names accepted by --version, and per program: (decomp.dev
category name, file name as passed to tools/xmatch.py, vram of xmatch offset 0, first file offset that belongs to
this program). The last field skips the X00 code that every JP area overlay repeats at its start (it is counted
once, in x00).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


JP_OVL = 0x800E9AF8   # retail JP overlay base (jal targets on prologues, like the demo estimate)
JP_SHARED = 0x2B680   # every JP X<nn>.BIN starts with these bytes of X00.BIN; the area part follows
USA_OVL = 0x800E7388  # retail USA overlay base (jal targets on X00 prologues; PAL 0x800E8028)
USA_SHARED = 0x2DE6C  # every USA X<nn>.BIN starts with these bytes of X00.BIN (like JP_SHARED)
# USA SYSTEM code overlays (SYSTEM/<NAME>.BIN, loaded at USA_OVL) -> the PAL module of tools/sysovl.py they pair with
USA_SYSOVL = {"dspsub": "d0spsub", "dspsub2": "d0spsub2", "dspsub3": "d0spsub3", "gover": "g0over",
              "info": "i0nfo", "info2": "i0nfo2", "info3": "i0nfo3", "optsub00": "o0ptsub0"}
# JP SYSTEM code overlays (same names as USA, no GOVER on the JP disc), loaded at JP_OVL
JP_SYSOVL = {p: m for p, m in USA_SYSOVL.items() if p != "gover"}

REFERENCE = "sces01331"
SERIALS = {"sces01331": "SCES_01331", "slps01144": "SLPS_01144", "slpm80165": "SLPM_80165", "pcpx96084": "PCPX_96084",
           "beta980203": "BETA_980203", "scus94236": "SCUS_94236"}
ALIASES = {"pal": "sces01331", "jp": "slps01144", "jpdemo": "slpm80165", "prepre8": "pcpx96084", "beta": "beta980203", "usa": "scus94236"}
BETA_OVL = 0x800EDAA8  # overlay base of the 1998-02-03 English preview (jal targets on X00 prologues)

VERSIONS = {
    "slpm80165": {
        "game": "game_jpdemo", "serial": "SLPM_80165",
        "progs": {"slpm80165": ("SLPM_801.65", "SLPM_801.65", 0x80010000, 0),
                  "x00": ("X00.BIN (SYSTEM)", "X00.BIN", 0x800E7698, 0)},
    },
    # PrePre Vol. 8 (PCPX-96084), Sony's Japanese demo compilation: the oldest known Tomba build (TOMBA/TOMBA.EXE,
    # one executable, no overlays). See docs/PREPRE8.md.
    "pcpx96084": {
        "game": "game_prepre8", "serial": "PCPX_96084",
        "progs": {"tomba": ("TOMBA.EXE (PrePre 8)", "TOMBA.EXE", 0x80010000, 0)},
    },
    # "Tomba! (Beta prototype) (1998-02-03)", CD-R "TOMBI NTSC Preview Version": English text, JP-style layout, boot
    # SLPS_011.44 (the JP serial, but a different executable). Serial-less, so the key is the build date. See
    # docs/BETA_980203.md.
    "beta980203": {
        "game": "game_beta980203", "serial": "BETA_980203",
        "progs": {"beta980203": ("SLPS_011.44 (beta 1998-02-03)", "SLPS_011.44", 0x80010000, 0),
                  "x00": ("X00.BIN (SYSTEM, beta)", "X00.BIN", BETA_OVL, 0)},
    },
    "slps01144": {
        "game": "game_jp", "serial": "SLPS_01144",
        "progs": dict([("slps01144", ("SLPS_011.44", "SLPS_011.44", 0x80010000, 0)),
                       ("x00", ("X00.BIN (AREA00)", "X00.BIN", JP_OVL, 0))]
                      + [("x%02d" % n, ("X%02d.BIN (AREA%02d)" % (n, n), "X%02d.BIN" % n, JP_OVL, JP_SHARED))
                         for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19)]
                      # SYSTEM code overlays: raw blobs at the area overlay base, see JP_SYSOVL
                      + [(p, ("%s.BIN (SYSTEM)" % p.upper(), "%s.BIN" % p.upper(), JP_OVL, 0)) for p in JP_SYSOVL]),
    },
    # USA retail "Tomba!" (SCUS-94236): the JP layout (two-digit X<nn>.BIN, shared X00 prefix). See docs/USA.md.
    "scus94236": {
        "game": "game_usa/fs", "serial": "SCUS_94236",
        "progs": dict([("scus94236", ("SCUS_942.36", "SCUS_942.36", 0x80010000, 0)),
                       ("x00", ("X00.BIN (AREA00)", "X00.BIN", USA_OVL, 0))]
                      + [("x%02d" % n, ("X%02d.BIN (AREA%02d)" % (n, n), "X%02d.BIN" % n, USA_OVL, USA_SHARED))
                         for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19)]
                      # SYSTEM code overlays: raw blobs at the area overlay base (PAL's at 0x800E8028), see USA_SYSOVL
                      + [(p, ("%s.BIN (SYSTEM)" % p.upper(), "%s.BIN" % p.upper(), USA_OVL, 0)) for p in USA_SYSOVL]),
    },
}

# PAL program whose src directory holds the shared C of a version program (main exe and X00 -> src/, xNN -> src/x0NN/)
def pal_prog(ver, prog):
    if prog in ("slps01144", "slpm80165", "tomba", "beta980203", "scus94236"): return "main0"
    if ver == "scus94236" and prog in USA_SYSOVL: return USA_SYSOVL[prog]
    if ver == "slps01144" and prog in JP_SYSOVL: return JP_SYSOVL[prog]
    return "x0" + prog[1:]


def pal_src_dir(ver, prog):
    p = pal_prog(ver, prog)
    return "src" if p in ("main0", "x000") else "src/" + p


# Sony's Psy-Q libraries are linked after the game in every version's main executable; their C lives in src/psyq/,
# apart from the game's (libc's rand.c beside the game's Rand.c is one file on a case-insensitive disk).
PSYQ_SRC = "src/psyq"
# The main executable's C: the game's, then the libraries'.
MAIN_SRC_DIRS = ("src", PSYQ_SRC)
# Per version, the lowest known library function of the main executable; everything from it up is library code.
PSYQ_START = {REFERENCE: 0x8005B934, "scus94236": 0x8005B38C, "slps01144": 0x8005844C, "slpm80165": 0x8005126C,
              "beta980203": 0x80059E84, "pcpx96084": 0x8008746C}


def is_psyq(ver, prog, addr):
    """Whether the function at `addr` of `prog` (a `// FUNC` or `// VERSION` program) is library code."""
    main = prog.lower() == "main0" if ver == REFERENCE else pal_prog(ver, prog) == "main0"
    return main and addr >= PSYQ_START[ver]


def src_dir(ver, prog, addr):
    """The directory a function's C goes in: src/psyq/ for library code, else its program's."""
    if is_psyq(ver, prog, addr):
        return PSYQ_SRC
    return "src" if ver == REFERENCE and prog.lower() in ("main0", "x000") else (
        "src/" + prog.lower() if ver == REFERENCE else pal_src_dir(ver, prog))


def target(ver, prog, addr, name):
    """The C file a function named `name` gets: <src_dir>/<name>.c, absolute."""
    return os.path.join(ROOT, src_dir(ver, prog, addr), name + ".c")


def taken(path):
    """The file a new `path` would clash with: one of the same name in its directory, letter case aside (Windows and macOS
    disks fold case, so two such names are one file there); None when the name is free."""
    d, name = os.path.split(path)
    for f in (os.listdir(d) if os.path.isdir(d) else ()):
        if f.lower() == name.lower():
            return os.path.join(d, f)
    return None


def main_sources():
    """Every .c file of the main executable's directories (and X000's, which shares src/), sorted by directory."""
    return [os.path.join(ROOT, d, f) for d in MAIN_SRC_DIRS if os.path.isdir(os.path.join(ROOT, d))
            for f in sorted(os.listdir(os.path.join(ROOT, d))) if f.endswith(".c")]


def canon(v):
    """Canonical version key (serial) for a --version value (serial, SLPS_01144 style, or old alias jp/jpdemo)."""
    v = v.lower().replace("_", "")
    v = ALIASES.get(v, v)
    if v != REFERENCE and v not in VERSIONS:
        raise SystemExit("unknown version %r (known: %s; aliases %s)" % (v, ", ".join([REFERENCE] + list(VERSIONS)),
                                                                          ", ".join(ALIASES)))
    return v


def version_arg(argv, default="slpm80165"):
    """Canonical value of --version in argv (default: the demo, for the original demo-only command lines)."""
    return canon(argv[argv.index("--version") + 1]) if "--version" in argv else default
