#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import specs.folly as folly
import specs.gmock as gmock
from shell_quoting import ShellQuoted


"fbcode_builder steps to build & test watchman"


def fbcode_builder_spec(builder):
    builder.add_option("watchman/_build:cmake_defines", {"BUILD_SHARED_LIBS": "OFF"})

    projects = builder.option("projects_dir")

    return {
        "depends_on": [gmock, folly],
        "steps": [
            builder.fb_github_cmake_install("watchman/_build", ".."),
            builder.step(
                "Run watchman tests",
                [
                    builder.run(
                        ShellQuoted("ctest --output-on-failure -j {n}").format(
                            n=builder.option("make_parallelism")
                        )
                    ),
                    builder.run(
                        ShellQuoted(
                            "cd ../ && ./runtests.py --concurrency {n} "
                            "--watchman-path _build/watchman --pybuild-dir {p}"
                        ).format(
                            n=builder.option("make_parallelism"),
                            p=os.path.join(projects, "watchman/_build/python"),
                        )
                    ),
                ],
            ),
        ],
    }


config = {
    "github_project": "facebook/watchman",
    "fbcode_builder_spec": fbcode_builder_spec,
}
