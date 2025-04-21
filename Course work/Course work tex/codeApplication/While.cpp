ABSL_LOG(INFO) << "Start grabbing and processing frames.";
bool GrabFrames = true;
while (GrabFrames)
{
    cv::Mat CameraFrame;
    capture >> CameraFrame;
    if (CameraFrame.empty())
    {
        ABSL_LOG(INFO) << "Ignore empty frames from camera.";
        continue;
    }
    cv::flip(CameraFrame, CameraFrame, /*flipcode=HORIZONTAL*/ 1);

    SendFrameToGraph(Graph, CameraFrame);

    cv::Mat OutputFrameMat = GetOutput(Poller);
    cv::imshow("Video Stylisation", OutputFrameMat);
    const int PressedKey = cv::waitKey(5);
    if (PressedKey >= 0 && PressedKey != 255) GrabFrames = false;
}