// https://github.com/react-dnd/react-dnd/tree/4d37ad5072ce8fb6a488a8672d5700676e643817/packages/documentation/examples/04%20Sortable/Simple

// BSD License

// Copyright (c) 2015, Facebook, Inc. All rights reserved.

// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:

//  * Redistributions of source code must retain the above copyright notice, this
//    list of conditions and the following disclaimer.

//  * Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution.

//  * Neither the name Facebook nor the names of its contributors may be used to
//    endorse or promote products derived from this software without specific
//    prior written permission.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
// ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
// ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import { useRef } from "react"
import { useDrag, useDrop } from "react-dnd"
import { connect } from "react-redux"

import { DragDrop, handleDndHover } from "@/dragDrop"
import ListItem from "@/pages/recipe-detail/ListItem"
import {
  deleteStep,
  IRecipe,
  IStep,
  updateStep,
} from "@/store/reducers/recipes"

interface IStepProps {
  readonly index: number
  readonly id: number
  readonly recipeID: IRecipe["id"]
  readonly text: string
  readonly move: (_: { from: number; to: number }) => void
  readonly completeMove: (_: { id: number; to: number }) => void
  readonly updating?: boolean
  readonly removing?: boolean
  readonly position?: string
  readonly isEditing: boolean
}

function Step({ text, index, ...props }: IStepProps) {
  const ref = useRef<HTMLDivElement>(null)
  const [, drop] = useDrop({
    accept: DragDrop.STEP,
    hover: handleDndHover({ ref, index, move: props.move }),
  })

  const [{ isDragging }, drag, preview] = useDrag({
    type: DragDrop.STEP,
    item: {
      index,
    },
    canDrag() {
      return props.isEditing
    },
    end: (draggedItem) => {
      props.completeMove({ id: props.id, to: draggedItem.index })
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  })

  const style = {
    backgroundColor: "white",
    opacity: isDragging ? 0 : 1,
  }

  preview(drop(ref))
  return (
    <div style={style} ref={props.isEditing ? ref : undefined} className="mb-2">
      <label
        className="better-label"
        ref={props.isEditing ? drag : undefined}
        style={{ cursor: props.isEditing ? "move" : "" }}
      >
        Step {index + 1}
      </label>
      <StepBody
        id={props.id}
        isEditing={props.isEditing}
        recipeID={props.recipeID}
        updating={props.updating}
        removing={props.removing}
        text={text}
      />
    </div>
  )
}

interface IStepBodyBasic {
  readonly id: IStep["id"]
  readonly recipeID: IRecipe["id"]
  readonly text: IStep["text"]
  readonly updating?: boolean
  readonly removing?: boolean
  readonly isEditing: boolean
  readonly update: (data: {
    recipeID: number
    stepID: number
    text?: string
  }) => void
  readonly remove: (data: { recipeID: IRecipe["id"]; stepID: number }) => void
}

function StepBodyBasic({
  recipeID,
  id,
  text,
  update,
  remove,
  updating,
  isEditing,
  removing,
}: IStepBodyBasic) {
  const listItemUpdate = (rID: number, sID: number, data: { text: string }) => {
    update({ recipeID: rID, stepID: sID, ...data })
  }

  return (
    <ListItem
      id={id}
      recipeID={recipeID}
      text={text}
      isEditing={isEditing}
      update={listItemUpdate}
      updating={updating}
      removing={removing}
      delete={() => {
        remove({ recipeID, stepID: id })
      }}
    />
  )
}

const StepBody = connect(null, {
  update: updateStep.request,
  remove: deleteStep.request,
})(StepBodyBasic)

export default Step
