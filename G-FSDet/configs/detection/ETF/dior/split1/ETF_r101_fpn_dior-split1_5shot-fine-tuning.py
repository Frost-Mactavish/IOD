_base_ = [
    '../../../_base_/datasets/fine_tune_based/few_shot_dior.py',
    '../../../_base_/schedules/schedule.py', '../../tfa_r101_fpn.py',
    '../../../_base_/default_runtime.py'
]
# classes splits are predefined in FewShotVOCDataset
# FewShotVOCDefaultDataset predefine ann_cfg for model reproducibility.
data = dict(
    train=dict(
        type='FewShotDIORDefaultDataset',
        ann_cfg=[dict(method='TFA', setting='SPLIT1_5SHOT')],
        num_novel_shots=5,
        num_base_shots=5,
        classes='ALL_CLASSES_SPLIT1'),
    val=dict(classes='ALL_CLASSES_SPLIT1'),
    test=dict(classes='ALL_CLASSES_SPLIT1'))
evaluation = dict(
    interval=6000,
    class_splits=['BASE_CLASSES_SPLIT1', 'NOVEL_CLASSES_SPLIT1'])
checkpoint_config = dict(interval=2000)
optimizer = dict(lr=0.001)
lr_config = dict(
    warmup_iters=100, step=[
        6000,
    ])
runner = dict(max_iters=6000)
model = dict(
    pretrained='open-mmlab://detectron2/resnet101_caffe',
    frozen_parameters=[
        'backbone', 'neck', 
    ],
    backbone=dict(depth=101),
    roi_head=dict(
        bbox_head=dict(
            num_classes=20)))
# base model needs to be initialized with following script:
#   tools/detection/misc/initialize_bbox_head.py
# please refer to configs/detection/tfa/README.md for more details.

load_from = ('work_dirs/DIOR/TFA/tfa_r101_fpn_dior-split1_base-training/'
             'base_model_random_init_bbox_head.pth')
