#pragma mark - MPPGraphDelegate methods

- (void)mediapipeGraph:(MPPGraph*)graph
    didOutputPixelBuffer:(CVPixelBufferRef)pixelBuffer
              fromStream:(const std::string&)streamName {
  if (streamName == kOutputStream) {
    NSLog(@"Received processed frame from output stream");
    [_delegate didProcessFrame:pixelBuffer];
  }
}