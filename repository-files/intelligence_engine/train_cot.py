"""
Supervised Fine-Tuning (SFT) with Chain-of-Thought Reasoning
Embeds Golden Thread reasoning into model weights with IP-04 Silent Flux integration.

The model learns to:
1. Generate internal reasoning chains
2. Cite specific legal frameworks (14 laws)
3. Pass through anxiety regulator before final output
4. Maintain humanitarian margin calculations
"""

import json
import os
import sys
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
import numpy as np
from tqdm import tqdm

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from governance_kernel.vector_ledger import SovereignGuardrail


@dataclass
class ChainOfThoughtExample:
    """Single training example with CoT reasoning"""
    input_context: str
    reasoning_chain: List[str]
    legal_citations: List[str]
    humanitarian_margin: float
    final_decision: str
    anxiety_level: float  # IP-04 Silent Flux


class HumanitarianDataset(Dataset):
    """PyTorch dataset for humanitarian training data"""
    
    def __init__(
        self,
        data_path: str,
        tokenizer,
        max_length: int = 2048,
        include_reasoning: bool = True
    ):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.include_reasoning = include_reasoning
        
        # Load data
        print(f"📂 Loading data from {data_path}...")
        self.examples = self._load_and_process_data(data_path)
        print(f"✅ Loaded {len(self.examples)} examples")
    
    def _load_and_process_data(self, data_path: str) -> List[ChainOfThoughtExample]:
        """Load JSONL data and convert to CoT examples"""
        examples = []
        
        with open(data_path, 'r') as f:
            for line in f:
                record = json.loads(line)
                
                # Generate CoT example from record
                cot_example = self._generate_cot_example(record)
                if cot_example:
                    examples.append(cot_example)
        
        return examples
    
    def _generate_cot_example(self, record: Dict) -> Optional[ChainOfThoughtExample]:
        """Generate Chain-of-Thought example from data record"""
        
        # Skip records without edge cases for now (focus on complex reasoning)
        if "edge_case" not in record:
            return None
        
        edge_case = record["edge_case"]
        
        # Build input context
        input_context = self._build_input_context(record)
        
        # Build reasoning chain
        reasoning_chain = self._build_reasoning_chain(record, edge_case)
        
        # Extract legal citations
        legal_citations = edge_case.get("legal_basis", [])
        
        # Get humanitarian margin
        humanitarian_margin = edge_case.get("humanitarian_margin", 0.0)
        
        # Get expected action
        final_decision = edge_case.get("expected_action", "UNKNOWN")
        
        # Calculate anxiety level (IP-04 Silent Flux)
        anxiety_level = self._calculate_anxiety_level(record)
        
        return ChainOfThoughtExample(
            input_context=input_context,
            reasoning_chain=reasoning_chain,
            legal_citations=legal_citations,
            humanitarian_margin=humanitarian_margin,
            final_decision=final_decision,
            anxiety_level=anxiety_level
        )
    
    def _build_input_context(self, record: Dict) -> str:
        """Build input context string"""
        location = record.get("location", {})
        clinical = record.get("clinical", {})
        demographics = record.get("demographics", {})
        
        context = f"""Patient Record Analysis Request:

Location: {location.get('name', 'Unknown')}, {location.get('country', 'Unknown')}
Jurisdiction: {record.get('jurisdiction', 'GLOBAL_DEFAULT')}

Demographics:
- Age: {demographics.get('age', 'Unknown')}
- Gender: {demographics.get('gender', 'Unknown')}
- Child: {demographics.get('is_child', False)}
- Refugee: {demographics.get('is_refugee', False)}

Clinical:
- Disease: {clinical.get('disease', 'Unknown')}
- Symptoms: {', '.join(clinical.get('symptoms', []))}
- Severity: {clinical.get('severity', 'Unknown')}/10
- Confidence: {clinical.get('diagnosis_confidence', 0.0):.2f}

Consent Status:
- Has Consent: {record.get('consent', {}).get('has_consent', False)}
- Scope: {record.get('consent', {}).get('consent_scope', 'None')}
- Guardian Required: {record.get('consent', {}).get('guardian_consent_required', False)}

Edge Case Scenario: {record.get('edge_case', {}).get('scenario', 'None')}
Description: {record.get('edge_case', {}).get('description', 'None')}

Question: What action should be taken? Provide step-by-step reasoning."""
        
        return context
    
    def _build_reasoning_chain(self, record: Dict, edge_case: Dict) -> List[str]:
        """Build step-by-step reasoning chain"""
        reasoning = []
        
        # Step 1: Identify the ethical conflict
        conflict = edge_case.get("conflict", "Unknown conflict")
        reasoning.append(f"STEP 1 - Identify Conflict: {conflict}")
        
        # Step 2: Consult relevant legal frameworks
        legal_basis = edge_case.get("legal_basis", [])
        reasoning.append(f"STEP 2 - Legal Framework: Consulting {', '.join(legal_basis)}")
        
        # Step 3: Calculate humanitarian margin
        margin = edge_case.get("humanitarian_margin", 0.0)
        reasoning.append(f"STEP 3 - Humanitarian Margin: {margin:.2f} (threshold: 0.15)")
        
        # Step 4: Apply conflict resolution hierarchy
        if margin >= 0.85:
            priority = "Life-saving interventions (ESR-07)"
        elif record.get('demographics', {}).get('is_child'):
            priority = "Child protection (ESR-13)"
        elif "sovereignty" in conflict.lower():
            priority = "Data sovereignty (ESR-01)"
        else:
            priority = "Standard compliance rules"
        
        reasoning.append(f"STEP 4 - Priority Rule: {priority}")
        
        # Step 5: Determine resolution
        resolution = edge_case.get("resolution", "Unknown resolution")
        reasoning.append(f"STEP 5 - Resolution: {resolution}")
        
        # Step 6: Final decision
        expected_action = edge_case.get("expected_action", "UNKNOWN")
        reasoning.append(f"STEP 6 - Decision: {expected_action}")
        
        return reasoning
    
    def _calculate_anxiety_level(self, record: Dict) -> float:
        """Calculate operator anxiety level for IP-04 Silent Flux"""
        # Factors that increase anxiety:
        # - High severity
        # - Child patient
        # - Emergency scenario
        # - Low confidence
        
        anxiety = 0.0
        
        # Severity contribution
        severity = record.get('clinical', {}).get('severity', 5)
        anxiety += (severity / 10.0) * 0.3
        
        # Child patient
        if record.get('demographics', {}).get('is_child'):
            anxiety += 0.2
        
        # Emergency scenario
        if "emergency" in record.get('edge_case', {}).get('scenario', '').lower():
            anxiety += 0.3
        
        # Low confidence
        confidence = record.get('clinical', {}).get('diagnosis_confidence', 1.0)
        if confidence < 0.7:
            anxiety += 0.2
        
        return min(anxiety, 1.0)
    
    def __len__(self) -> int:
        return len(self.examples)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """Get tokenized example"""
        example = self.examples[idx]
        
        # Build full text with CoT reasoning
        if self.include_reasoning:
            full_text = f"""{example.input_context}

INTERNAL REASONING CHAIN:
{chr(10).join(example.reasoning_chain)}

LEGAL CITATIONS:
{', '.join(example.legal_citations)}

HUMANITARIAN MARGIN: {example.humanitarian_margin:.2f}

ANXIETY LEVEL (IP-04 Silent Flux): {example.anxiety_level:.2f}
{'[OUTPUT VERBOSITY REDUCED DUE TO HIGH ANXIETY]' if example.anxiety_level > 0.7 else ''}

FINAL DECISION: {example.final_decision}
"""
        else:
            full_text = f"{example.input_context}\n\nFINAL DECISION: {example.final_decision}"
        
        # Tokenize
        encoding = self.tokenizer(
            full_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": encoding["input_ids"].squeeze()  # For causal LM
        }


class SpiralAGITrainer:
    """Trainer for Spiral AGI with CoT reasoning"""
    
    def __init__(
        self,
        model_name: str = "gpt2",  # Can use larger models like "meta-llama/Llama-2-7b-hf"
        output_dir: str = "./models/spiral_agi",
        data_dir: str = "./data/synthetic"
    ):
        self.model_name = model_name
        self.output_dir = output_dir
        self.data_dir = data_dir
        
        # Initialize tokenizer and model
        print(f"🤖 Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        print(f"✅ Model loaded: {self.model.num_parameters():,} parameters")
        
        # Initialize SovereignGuardrail for validation
        self.guardrail = SovereignGuardrail()
    
    def prepare_datasets(self) -> Tuple[Dataset, Dataset]:
        """Prepare train and validation datasets"""
        data_path = os.path.join(self.data_dir, "humanitarian_training_data.jsonl")
        
        # Load full dataset
        full_dataset = HumanitarianDataset(
            data_path=data_path,
            tokenizer=self.tokenizer,
            include_reasoning=True
        )
        
        # Split into train/val (90/10)
        train_size = int(0.9 * len(full_dataset))
        val_size = len(full_dataset) - train_size
        
        train_dataset, val_dataset = torch.utils.data.random_split(
            full_dataset,
            [train_size, val_size]
        )
        
        print(f"📊 Dataset split:")
        print(f"   Train: {len(train_dataset)} examples")
        print(f"   Val: {len(val_dataset)} examples")
        
        return train_dataset, val_dataset
    
    def train(
        self,
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-5,
        warmup_steps: int = 500,
        save_steps: int = 1000
    ):
        """Train the model with SFT"""
        print("🚀 Starting Supervised Fine-Tuning...")
        
        # Prepare datasets
        train_dataset, val_dataset = self.prepare_datasets()
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=warmup_steps,
            learning_rate=learning_rate,
            fp16=torch.cuda.is_available(),
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=100,
            save_steps=save_steps,
            eval_steps=save_steps,
            evaluation_strategy="steps",
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            report_to="tensorboard",
            gradient_accumulation_steps=4,
            gradient_checkpointing=True,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # Causal LM, not masked LM
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
        )
        
        # Train
        print("🔥 Training started...")
        trainer.train()
        
        # Save final model
        print("💾 Saving final model...")
        trainer.save_model(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        
        print("✅ Training complete!")
        print(f"   Model saved to: {self.output_dir}")
    
    def generate_reasoning(
        self,
        input_context: str,
        max_length: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """Generate CoT reasoning for input"""
        # Tokenize input
        inputs = self.tokenizer(input_context, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return generated_text


def main():
    """Main training execution"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   iLuminara Spiral AGI - Chain-of-Thought Training         ║")
    print("║   Supervised Fine-Tuning with IP-04 Silent Flux            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Check for GPU
    if torch.cuda.is_available():
        print(f"🎮 GPU detected: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("⚠️  No GPU detected - training will be slow")
    print()
    
    # Initialize trainer
    trainer = SpiralAGITrainer(
        model_name="gpt2",  # Start with GPT-2, can upgrade to Llama-2
        output_dir="./models/spiral_agi_cot",
        data_dir="./data/synthetic"
    )
    
    # Train
    trainer.train(
        num_epochs=3,
        batch_size=4,
        learning_rate=2e-5
    )
    
    print()
    print("🎯 Next steps:")
    print("   1. Evaluate model: python tests/evaluate_spiral_agi.py")
    print("   2. Run RL optimization: python intelligence_engine/rl_optimizer.py")
    print("   3. Deploy to production: python deploy_spiral_agi.py")


if __name__ == "__main__":
    main()
