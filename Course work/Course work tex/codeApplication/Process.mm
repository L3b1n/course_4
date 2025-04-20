#pragma mark - MPPInputSourceDelegate methods

- (void)processVideoFrame:(CVPixelBufferRef)imageBuffer {
  const auto ts =
      mediapipe::Timestamp(self.timestamp++ * mediapipe::Timestamp::kTimestampUnitsPerSecond);
  NSError* err = nil;
  NSLog(@"Sending frame @%@ to %s", @(ts.DebugString().c_str()), kInputStream);
  auto sent = [self.mediapipeGraph sendPixelBuffer:imageBuffer
                                   intoStream:kInputStream
                                   packetType:MPPPacketTypePixelBuffer
                                   timestamp:ts
                                   allowOverwrite:NO
                                   error:&err];
  NSLog(@"Frame %s", sent ? "sent!" : "not sent.");
  if (err) {
    NSLog(@"Error sending frame: %@", err);
  }
}