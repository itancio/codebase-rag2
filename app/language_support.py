
class LanguageSupport:
    # Class-level dictionary to store file extensions and their languages
    lang_map = {
        ".cpp": "cpp",
        ".go": "go",
        ".java": "java",
        ".kt": "kotlin",
        ".js": "js",
        ".jsx": "js",
        ".ts": "ts",
        ".tsx": "ts",
        ".php": "php",
        ".proto": "proto",
        ".py": "python",
        ".rst": "rst",
        ".rb": "ruby",
        ".rs": "rust",
        ".scala": "scala",
        ".swift": "swift",
        ".md": "markdown",
        ".tex": "latex",
        ".html": "html",
        ".sol": "sol",
        ".cs": "csharp",
        ".cobol": "cobol",
        ".c": "c",
        ".lua": "lua",
        ".pl": "perl",
        ".hs": "haskell",
        ".ipynb": "ipynb"   # Not supported language for codeSplitter
    }

    @classmethod
    def is_supported_language(cls, extension):
        """Check if the given file extension is supported."""
        return extension in cls.lang_map

    @classmethod
    def get_language(cls, extension):
        """Get the language associated with a file extension."""
        return cls.lang_map.get(extension, "Unsupported language")

    @classmethod
    def add_language(cls, extension, language):
        """Add a new file extension and associated language."""
        cls.lang_map[extension] = language

    @classmethod
    def remove_language(cls, extension):
        """Remove a file extension from the mapping."""
        if extension in cls.lang_map:
            del cls.lang_map[extension]
