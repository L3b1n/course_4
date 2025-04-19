#import <CoreVideo/CoreVideo.h>
#import <Foundation/Foundation.h>

@protocol VideoProcessingDelegate <NSObject>
@optional
- (void)didProcessFrame:(CVPixelBufferRef)outputBuffer;
@end

@interface VideoProcessor : NSObject
- (instancetype)init;
- (void)startGraph;
- (void)processVideoFrame:(CVPixelBufferRef)imageBuffer;
@property(weak, nonatomic) id<VideoProcessingDelegate> delegate;
@property(nonatomic) size_t timestamp;
@end