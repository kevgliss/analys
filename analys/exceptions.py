class AnalysException(Exception):
    pass

class ResourceNotFound(AnalysException):
    pass

class InvalidResourceType(AnalysException):
    pass

class MimeTypeNotFound(AnalysException):
    pass

class EmptyCompressedFile(AnalysException):
    pass

class MaxFileDepth(AnalysException):
    pass

class NoValidPasswordFound(AnalysException):
    pass

class InvalidMimeType(AnalysException):
    pass
