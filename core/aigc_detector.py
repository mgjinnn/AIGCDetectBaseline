import numpy as np
import os
import random
import torch
import torch.utils.data

from copy import deepcopy
from sklearn.metrics import average_precision_score, precision_recall_curve, accuracy_score

from .dataset import RealFakeDataset
from .models import get_model


SEED = 0
def set_seed():
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    np.random.seed(SEED)
    random.seed(SEED)


def calculate_acc(y_true, y_pred, thres):
    r_acc = accuracy_score(y_true[y_true==0], y_pred[y_true==0] > thres)
    f_acc = accuracy_score(y_true[y_true==1], y_pred[y_true==1] > thres)
    acc = accuracy_score(y_true, y_pred > thres)
    return r_acc, f_acc, acc    


def find_best_threshold(y_true, y_pred):
    "We assume first half is real 0, and the second half is fake 1"

    N = y_true.shape[0]

    if y_pred[0:N//2].max() <= y_pred[N//2:N].min(): # perfectly separable case
        return (y_pred[0:N//2].max() + y_pred[N//2:N].min()) / 2 

    best_acc = 0 
    best_thres = 0 
    for thres in y_pred:
        temp = deepcopy(y_pred)
        temp[temp>=thres] = 1 
        temp[temp<thres] = 0 

        acc = (temp == y_true).sum() / N  
        if acc >= best_acc:
            best_thres = thres
            best_acc = acc 
    
    return best_thres

    
class AIGCDetector:

    def __init__(self):
        self.arch = 'CLIP:ViT-L/14'
        ckpt = 'core/weights/fc_weights.pth'

        self.data_mode = 'wang2020'
        self.batch_size = 8

        self.model = get_model(self.arch)
        state_dict = torch.load(ckpt, map_location='cpu')
        self.model.fc.load_state_dict(state_dict)
        print ("@@@ Model loaded..")
        self.model.eval()
        self.model.cuda()


    def val(self, data_path):
        real_path = os.path.join(data_path, '0_real')
        fake_path = os.path.join(data_path, '1_fake')

        dataset_path = dict(real_path=real_path, fake_path=fake_path, data_mode=self.data_mode)
        
        set_seed()
        dataset = RealFakeDataset(dataset_path['real_path'], dataset_path['fake_path'], dataset_path['data_mode'], self.arch)
        print(f'@@@ len(dataset): {len(dataset)}')

        loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=False, num_workers=4)
        ap, r_acc0, f_acc0, acc0, r_acc1, f_acc1, acc1, best_thres = self.validate(self.model, loader)
        
        return ap, len(dataset)

    def validate(self, model, loader):
        with torch.no_grad():
            y_true, y_pred = [], []
            print ("Length of dataset: %d" %(len(loader)))
            for img, label in loader:
                in_tens = img.cuda()

                y_pred.extend(model(in_tens).sigmoid().flatten().tolist())
                y_true.extend(label.flatten().tolist())

        y_true, y_pred = np.array(y_true), np.array(y_pred)

        # ================== save this if you want to plot the curves =========== # 
        # torch.save( torch.stack( [torch.tensor(y_true), torch.tensor(y_pred)] ),  'baseline_predication_for_pr_roc_curve.pth' )
        # exit()
        # =================================================================== #
        
        # Get AP 
        ap = average_precision_score(y_true, y_pred)

        # Acc based on 0.5
        r_acc0, f_acc0, acc0 = calculate_acc(y_true, y_pred, 0.5)

        # Acc based on the best thres
        best_thres = find_best_threshold(y_true, y_pred)
        r_acc1, f_acc1, acc1 = calculate_acc(y_true, y_pred, best_thres)

        return ap, r_acc0, f_acc0, acc0, r_acc1, f_acc1, acc1, best_thres