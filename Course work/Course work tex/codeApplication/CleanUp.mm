#pragma mark - Cleanup methods

- (void)dealloc {
  self.mediapipeGraph.delegate = nil;
  [self.mediapipeGraph cancel];
  [self.mediapipeGraph closeAllInputStreamsWithError:nil];
  [self.mediapipeGraph waitUntilDoneWithError:nil];
}