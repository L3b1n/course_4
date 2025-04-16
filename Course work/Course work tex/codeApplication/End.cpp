ABSL_LOG(INFO) << "Shutting down.";
MP_RETURN_IF_ERROR(graph.CloseInputStream("input_video"));
graph.WaitUntilDone();