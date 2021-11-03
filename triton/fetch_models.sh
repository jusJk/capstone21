set -ex

# LPDnet USA
wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/tlt_lpdnet/versions/pruned_v1.0/zip -O /tmp/tlt_lpdnet_pruned_v1.0.zip
(cd /tmp && unzip tlt_lpdnet_pruned_v1.0.zip)
mv /tmp/usa_pruned.etlt ./model_repository/lpdnet_usa/usa_pruned.etlt

# LPRnet USA
wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/tlt_lprnet/versions/deployable_v1.0/zip -O /tmp/tlt_lprnet_deployable_v1.0.zip
(cd /tmp && unzip tlt_lprnet_deployable_v1.0.zip)
mv /tmp/us_lprnet_baseline18_deployable.etlt ./model_repository/lprnet_usa/us_lprnet_baseline18_deployable.etlt

# BodyposeNet
wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/tao/bodyposenet/versions/deployable_v1.0.1/zip -O /tmp/bodyposenet_deployable_v1.0.1.zip
(cd /tmp && unzip bodyposenet_deployable_v1.0.1.zip)
mv /tmp/model.etlt ./model_repository/bodyposenet/model.etlt

# TrafficCamNet
wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0.1/zip -O /tmp/trafficcamnet_pruned_v1.0.1.zip
(cd /tmp && unzip trafficcamnet_pruned_v1.0.1.zip)
mv /tmp/resnet18_trafficcamnet_pruned.etlt ./model_repository/trafficcamnet/resnet18_trafficcamnet_pruned.etlt