from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibFlannConan(ConanFile):
    name = "flann"
    version = "1.9.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeProjectWrapper.txt",
        "patches/flann_cmake_311.diff"
    ]
    url = "https://gitlab.lan.local/conan/conan-flann"
    license="BSD License"
    description = "Fast Library for Approximate Nearest Neighbors."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def source(self):
        tools.get("https://github.com/mariusmuja/flann/archive/{0}.tar.gz".format(self.version))
        os.rename("flann-" + self.version, self.source_subfolder)

    def build(self):
        flann_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")
        tools.patch(flann_source_dir, "patches/flann_cmake_311.diff")

        cmake = CMake(self)
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_DOC"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_C_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_MATLAB_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = "OFF"

        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
