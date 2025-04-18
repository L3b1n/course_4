ABSL_LOG(INFO) << "Initialize the GPU.";
MP_ASSIGN_OR_RETURN(auto GpuResources, mediapipe::GpuResources::Create());
MP_RETURN_IF_ERROR(Graph.SetGpuResources(std::move(GpuResources)));
mediapipe::GlCalculatorHelper GpuHelper;
GpuHelper.InitializeForTest(Graph.GetGpuResources().get());