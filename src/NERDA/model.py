from .utils import get_bert_model
import torch
import torch.nn as nn
import transformers

class NER_BERT(nn.Module):
    def __init__(self, bert_model_name, device, n_tags):
        super(NER_BERT, self).__init__()
        self.bert = get_bert_model(bert_model_name) 
        self.dropout = nn.Dropout(0.1)
        # TODO: overvej at parametrisere n_tags
        self.tags = nn.Linear(768, n_tags)
        self.device = device

    # NOTE: offsets not used as-is, but is expected as output
    # down-stream. So don't remove! :)

    def forward(self, ids, masks, token_type_ids, target_tags, offsets):

        # move tensors to device
        ids = ids.to(self.device)
        masks = masks.to(self.device)
        token_type_ids = token_type_ids.to(self.device)
        target_tags = target_tags.to(self.device)

        outputs, _ = self.bert(ids, attention_mask = masks, token_type_ids = token_type_ids)

        # apply drop-out
        outputs = self.dropout(outputs)

        # outputs for all labels/tags
        outputs = self.tags(outputs)

        return outputs