#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import re
from conans import ConanFile, CMake, tools


class ProtobuftestConan(ConanFile):
    name = "protobuf-test"
    version = "3.6.1"
    license = "MIT"
    author = "Bincrafters <bincrafters@gmail.com>"
    url = "https://github.com/bincrafters/protobuf-integration-test"
    description = "Run integration tests for Protobuf and Protoc"
    topics = ("conan", "protobuf", "protoc", "testing")
    settings = "os", "compiler", "build_type", "arch"
    options = {"testing": [True, False]}
    default_options = {"testing": True}
    generators = "cmake"
    exports = "LICENSE.md"
    exports_sources = ("src/*", "CMakeLists.txt")
    build_requires = "protoc_installer/3.6.1@bincrafters/stable"
    requires = "protobuf/3.6.1@bincrafters/stable"

    def requirements(self):
        if self.options.testing:
            self.requires("Catch2/2.5.0@catchorg/stable")

    def _test_arm(self):
        bin_path = os.path.join(self.build_folder, "bin", self.name)
        output = subprocess.check_output(["readelf", "-h", bin_path]).decode()
        assert re.search(r"Machine:\s+ARM", output)

    def build(self):
        cmake = CMake(self, set_cmake_flags=True)
        cmake.configure(source_folder="src")
        cmake.build()
        if self.options.testing:
            if tools.cross_building(self.settings) and "arm" in self.settings.arch:
                self._test_arm()
            else:
                cmake.test()

    def package(self):
        pass