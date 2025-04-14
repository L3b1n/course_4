import ARKit
import AVFoundation

class Camera: NSObject {
    enum CameraPosition {
        case front
        case back
    }
    private(set) var currentPosition: CameraPosition = .front

    lazy var session: AVCaptureSession = .init()
    private var device: AVCaptureDevice?
    private var input: AVCaptureDeviceInput?
    lazy var output: AVCaptureVideoDataOutput = .init()
    
    override init() {
        super.init()
        configureSession(for: currentPosition)
    }
    
    private func configureSession(for position: CameraPosition) {
        session.beginConfiguration()
        defer { session.commitConfiguration() }
        
        if let existingInput = input {
            session.removeInput(existingInput)
        }

        let newPosition: AVCaptureDevice.Position = position == .front ? .front : .back
        if let newDevice = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: newPosition),
           let newInput = try? AVCaptureDeviceInput(device: newDevice) {
            
            self.device = newDevice
            self.input = newInput
            
            if session.canAddInput(newInput) {
                session.addInput(newInput)
            }
        }
        
        if session.outputs.isEmpty {
            output.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]
            if session.canAddOutput(output) {
                session.addOutput(output)
            }
        }
    }
    
    func switchCamera() {
        currentPosition = (currentPosition == .front) ? .back : .front
        configureSession(for: currentPosition)
    }
    
    func setSampleBufferDelegate(_ delegate: AVCaptureVideoDataOutputSampleBufferDelegate) {
        output.setSampleBufferDelegate(delegate, queue: .main)
    }

    func start() {
        if !session.isRunning {
            session.startRunning()
        }
    }

    func stop() {
        if session.isRunning {
            session.stopRunning()
        }
    }
}
