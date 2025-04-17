cv::Mat GetOutput(mediapipe::OutputStreamPoller& Poller)
{
    mediapipe::Packet Packet;
    if (!Poller.Next(&Packet)) break;
    auto& OutputFrame = Packet.Get<mediapipe::ImageFrame>();

    return mediapipe::formats::MatView(&OutputFrame);
}