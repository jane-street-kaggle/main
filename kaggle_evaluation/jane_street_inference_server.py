
import jane_street_gateway

import kaggle_evaluation.core.templates


class JSInferenceServer(kaggle_evaluation.core.templates.InferenceServer):
    def _get_gateway_for_test(self, data_paths=None):
        return jane_street_gateway.JSGateway(data_paths)
