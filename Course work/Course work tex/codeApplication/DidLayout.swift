override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    displayLayer.frame = cameraView.bounds
}

@objc private func didTapSwitchCamera() {
    camera.switchCamera()
}