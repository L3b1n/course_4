ABSL_LOG(INFO) << "Start running the calculator graph.";
MP_ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller Poller,
                    Graph.AddOutputStreamPoller("output_video"));
MP_RETURN_IF_ERROR(Graph.StartRun({}));