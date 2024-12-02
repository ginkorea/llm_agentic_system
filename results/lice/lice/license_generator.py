from .models.license_file import LicenseFile
from .template_manager import TemplateManager
from .language_detector import LanguageDetector

class LicenseGenerator:
    def __init__(self):
        self.template_manager = TemplateManager()
        self.language_detector = LanguageDetector()

    def generateLicense(self, type, year, org):
        template = self.template_manager.getTemplate(type)
        language = self.language_detector.detectLanguage("py")  # Example extension
        content = f"{template} for {org} in {year} using {language}"
        return LicenseFile(type, year, org, content)

    def listAvailableLicenses(self):
        return self.template_manager.listTemplates()

    def addCustomTemplate(self, templatePath):
        return self.template_manager.addTemplate(templatePath)