override func viewDidLoad() {
    super.viewDidLoad()

    view.addSubview(imgView)
    view.addSubview(switchCameraButton)

    NSLayoutConstraint.activate([
        imgView.topAnchor.constraint(equalTo: view.topAnchor),
        imgView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
        imgView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
        imgView.bottomAnchor.constraint(equalTo: view.bottomAnchor),

        switchCameraButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -20),
        switchCameraButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
        switchCameraButton.widthAnchor.constraint(equalToConstant: 150),
        switchCameraButton.heightAnchor.constraint(equalToConstant: 50),
    ])

    camera.setSampleBufferDelegate(self)
    camera.start()
    videoProcessor.startGraph()
    videoProcessor.delegate = self
}