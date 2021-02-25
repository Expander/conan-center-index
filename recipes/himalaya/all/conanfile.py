import os
from conans import ConanFile, CMake, tools

required_conan_version = ">=1.30.0"


class HimalayaConan(ConanFile):
    name = "himalaya"
    license = "GPL-3.0-only"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/Himalaya-Library/Himalaya"
    description = "C++ library to calculate three-loop corrections to the Higgs boson mass in the MSSM"
    topics = ("conan", "high-energy", "physics", "hep", "Higgs", "mass", "MSSM")
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("Himalaya does not support {}".format(self.settings.compiler))

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.requires("eigen/3.3.9")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("Himalaya-{}".format(self.version), self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Himalaya"
        self.cpp_info.names["cmake_find_package_multi"] = "Himalaya"
        self.cpp_info.names["pkg_config"] = "himalaya"
        self.cpp_info.libs = ["Himalaya", "DSZ"]
        self.cpp_info.requires = ["eigen::eigen"]
