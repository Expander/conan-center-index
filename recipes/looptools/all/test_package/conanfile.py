import os

from conans import ConanFile, CMake, tools


class LooptoolsTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(os.path.join("bin", "test_package_f"), run_environment=True)
            self.run(os.path.join("bin", "test_package_c"), run_environment=True)
