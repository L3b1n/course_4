load("@build_bazel_rules_apple//apple:ios.bzl", "ios_application", "ios_framework")
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")
load(
    "//mediapipe/examples/ios:bundle_id.bzl",
    "BUNDLE_ID_PREFIX",
    "example_provisioning",
)

licenses(["notice"])  # Apache 2.0

MIN_IOS_VERSION = "17.6"

IOS_FAMILIES = [
    "iphone",
    "ipad",
]

ios_framework(
    name = "Stylising",
    hdrs = FRAMEWORK_HEADERS,
    bundle_id = BUNDLE_ID_PREFIX + ".StylisingFramework",
    bundle_name = "Stylising",
    families = IOS_FAMILIES,
    infoplists = [
        "//mediapipe/examples/ios/common:Info.plist",
    ],
    minimum_os_version = MIN_IOS_VERSION,
    visibility = ["//visibility:public"],
    deps = [
        ":ObjcppLib",
        "@ios_opencv//:OpencvFramework",
    ],
)

objc_library(
    name = "ObjcppLib",
    srcs = [
        "ObjcppLib.mm",
    ],
    hdrs = FRAMEWORK_HEADERS,
    copts = ["-std=c++17"],
    data = [
        "//mediapipe/examples/Stylising/graphs:Stylising_gpu.binarypb",
        "//mediapipe/models/whitebox_cartoon_gan_540x960_fp16.tflite",
    ],
    deps = [
        "//mediapipe/objc:mediapipe_framework_ios",
        "//mediapipe/objc:mediapipe_input_sources_ios",
        "//mediapipe/objc:mediapipe_layer_renderer",
    ] + select({
        "//conditions:default": [
            "//mediapipe/examples/Stylising/graphs:gpu_calculators",
        ],
    }),
)