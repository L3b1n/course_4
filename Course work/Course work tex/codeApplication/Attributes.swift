let camera = Camera()
let displayLayer: AVSampleBufferDisplayLayer = .init()
let videoProcessor: VideoProcessor = VideoProcessor()!

private lazy var cameraView: UIView = {
    let view = UIView()
    view.translatesAutoresizingMaskIntoConstraints = false
    return view
}()

private lazy var imgView: UIImageView = {
    let imageView = UIImageView()
    imageView.translatesAutoresizingMaskIntoConstraints = false
    imageView.contentMode = .scaleAspectFill
    return imageView
}()

private lazy var switchCameraButton: UIButton = {
    let button = UIButton(type: .system)
    button.translatesAutoresizingMaskIntoConstraints = false
    button.setTitle("Switch Camera", for: .normal)
    button.setTitleColor(.white, for: .normal)
    button.backgroundColor = UIColor.black.withAlphaComponent(0.5)
    button.layer.cornerRadius = 10
    button.addTarget(self, action: #selector(didTapSwitchCamera), for: .touchUpInside)
    return button
}()