void SendFrameToGraph(mediapipe::CalculatorGraph& Graph, cv::Mat& CameraFrame)
{
    auto InputFrame = absl::make_unique<mediapipe::ImageFrame>(
        mediapipe::ImageFormat::SRGB, CameraFrame.cols, CameraFrame.rows,
        mediapipe::ImageFrame::kDefaultAlignmentBoundary);
    cv::Mat InputFrameMat = mediapipe::formats::MatView(InputFrame.get());
    CameraFrame.copyTo(InputFrameMat);

    size_t FrameTimestampUs =
        (double)cv::getTickCount() / (double)cv::getTickFrequency() * 1e6;
    MP_RETURN_IF_ERROR(graph.AddPacketToInputStream(
        "input_video", mediapipe::Adopt(InputFrame.release())
                            .At(mediapipe::Timestamp(FrameTimestampUs))));
}