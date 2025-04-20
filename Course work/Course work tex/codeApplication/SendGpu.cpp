void SendFrameToGraph(mediapipe::CalculatorGraph& Graph, cv::Mat& CameraFrame)
{
    cv::cvtColor(CameraFrame, CameraFrame, cv::COLOR_BGR2BGRA);

    auto InputFrame = absl::make_unique<mediapipe::ImageFrame>(
        mediapipe::ImageFormat::SRGBA, CameraFrame.cols, CameraFrame.rows,
        mediapipe::ImageFrame::kGlDefaultAlignmentBoundary);
    cv::Mat InputFrameMat = mediapipe::formats::MatView(InputFrame.get());
    CameraFrame.copyTo(InputFrameMat);

    size_t FrameTimestampUs =
        (double)cv::getTickCount() / (double)cv::getTickFrequency() * 1e6;
    MP_RETURN_IF_ERROR(
        GpuHelper.RunInGlContext(
            [&InputFrame, &FrameTimestampUs, &Graph, &GpuHelper]() -> absl::Status {
                auto Texture = GpuHelper.CreateSourceTexture(*InputFrame.get());
                auto GpuFrame = Texture.GetFrame<mediapipe::GpuBuffer>();
                glFlush();
                Texture.Release();
                MP_RETURN_IF_ERROR(Graph.AddPacketToInputStream(
                    "input_video", mediapipe::Adopt(GpuFrame.release())
                                    .At(mediapipe::Timestamp(FrameTimestampUs))));
                return absl::OkStatus();
            }
        )
    );
}