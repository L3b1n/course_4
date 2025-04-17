cv::Mat GetOutputGpu(mediapipe::OutputStreamPoller& Poller)
{
    mediapipe::Packet Packet;
    if (!Poller.Next(&Packet)) break;
    std::unique_ptr<mediapipe::ImageFrame> OutputFrame;

    MP_RETURN_IF_ERROR(GpuHelper.RunInGlContext(
            [&Packet, &OutputFrame, &GpuHelper]() -> absl::Status {
                auto& GpuFrame = Packet.Get<mediapipe::GpuBuffer>();
                auto Texture = GpuHelper.CreateSourceTexture(GpuFrame);
                OutputFrame = absl::make_unique<mediapipe::ImageFrame>(
                    mediapipe::ImageFormatForGpuBufferFormat(GpuFrame.format()),
                    GpuFrame.width(), GpuFrame.height(),
                    mediapipe::ImageFrame::kGlDefaultAlignmentBoundary);
                GpuHelper.BindFramebuffer(Texture);
                const auto Info = mediapipe::GlTextureInfoForGpuBufferFormat(
                    GpuFrame.format(), 0, GpuHelper.GetGlVersion());
                glReadPixels(0, 0, texture.width(), texture.height(), Info.gl_format, Info.gl_type, OutputFrame->MutablePixelData());
                glFlush();
                Texture.Release();
                return absl::OkStatus();
            }
        )
    );

    cv::Mat OutputFrameMat = mediapipe::formats::MatView(OutputFrame.get());
    if (OutputFrameMat.channels() == 4)
        cv::cvtColor(OutputFrameMat, OutputFrameMat, cv::COLOR_RGBA2RGBA);
    return OutputFrameMat;
}