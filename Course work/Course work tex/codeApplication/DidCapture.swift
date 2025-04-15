func captureOutput(
    _ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer,
    from connection: AVCaptureConnection
) {
    connection.videoOrientation = .portrait
    displayLayer.enqueue(sampleBuffer)
    let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer)
    videoProcessor.processVideoFrame(pixelBuffer)
}