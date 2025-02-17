from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibFlannConan(ConanFile):
    python_requires = "camp_common/[>=0.1]@camposs/stable"

    name = "flann"
    package_revision = "-r7"
    upstream_version = "1.9.1"
    version = "{0}{1}".format(upstream_version, package_revision)

    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeProjectWrapper.txt",
        "patches/flann_cmake_311.diff",
        "patches/c++17_support.diff",
        "patches/FindFLANN.cmake"
    ]
    url = "https://github.com/ulricheck/conan-flann"
    license="BSD License"
    description = "Fast Library for Approximate Nearest Neighbors."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("https://github.com/mariusmuja/flann/archive/{0}.tar.gz".format(self.upstream_version))
        os.rename("flann-" + self.upstream_version, self.source_subfolder)

    def build(self):
        flann_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        tools.patch(flann_source_dir, "patches/flann_cmake_311.diff")
        tools.patch(flann_source_dir, "patches/c++17_support.diff")
        # Import common flags and defines
        common = self.python_requires["camp_common"].module

        flann_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")
        tools.patch(flann_source_dir, "patches/flann_cmake_311.diff")

        cmake = CMake(self)
        
        # Set common flags
        cmake.definitions["SIGHT_CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_DOC"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_C_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_MATLAB_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = "OFF"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("patches/FindFLANN.cmake", src=".", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
