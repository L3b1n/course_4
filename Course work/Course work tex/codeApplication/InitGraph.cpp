std::string CalculatorGraphConfigContents;
MP_RETURN_IF_ERROR(mediapipe::file::GetContents(
    absl::GetFlag(FLAGS_calculator_graph_config_file),
    &CalculatorGraphConfigContents));
ABSL_LOG(INFO) << "Get calculator graph config contents: "
                << CalculatorGraphConfigContents;
mediapipe::CalculatorGraphConfig Config =
    mediapipe::ParseTextProtoOrDie<mediapipe::CalculatorGraphConfig>(
        CalculatorGraphConfigContents);

ABSL_LOG(INFO) << "Initialize the calculator graph.";
mediapipe::CalculatorGraph Graph;
MP_RETURN_IF_ERROR(Graph.Initialize(Config));

ABSL_LOG(INFO) << "Initialize the camera or load the video.";
cv::VideoCapture capture;
capture.open(0);
RET_CHECK(capture.isOpened());

cv::namedWindow(kWindowName, /*flags=WINDOW_AUTOSIZE*/ 1);
#if (CV_MAJOR_VERSION >= 3) && (CV_MINOR_VERSION >= 2)
capture.set(cv::CAP_PROP_FRAME_WIDTH, 640);
capture.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
capture.set(cv::CAP_PROP_FPS, 30);
#endif