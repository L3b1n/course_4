func didProcessFrame(_ outputBuffer: CVPixelBuffer) {
    DispatchQueue.main.async {
        let ciImage = CIImage(cvPixelBuffer: outputBuffer)
        let uiImage = UIImage(ciImage: ciImage)
        self.imgView.contentMode = .scaleAspectFill
        self.imgView.image = uiImage
    }
}