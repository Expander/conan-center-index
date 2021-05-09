import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools

required_conan_version = ">=1.30.0"


class Gm2calcConan(ConanFile):
    name = "looptools"
    license = "GPL-3.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://www.feynarts.de/looptools/"
    description = "Fortran library for the numerical evaluation of one-loop scalar and tensor integrals"
    topics = ("conan", "high-energy", "physics", "hep", "one-loop", "integrals")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake", "cmake_find_package"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("LoopTools-{}".format(self.version), self._source_subfolder)

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(self)
        self._autotools.configure(build=False,
                                  host=False,
                                  configure_dir=self._source_subfolder)
        self._autotools.make()
        return self._autotools

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rename(os.path.join(self.package_folder, "lib64"),
                     os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "LoopTools"
        self.cpp_info.names["cmake_find_package_multi"] = "LoopTools"
        self.cpp_info.names["pkg_config"] = "looptools"
        self.cpp_info.libs = ["ooptools", "gfortran"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
